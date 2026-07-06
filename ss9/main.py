from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Cinema Ticket Booking API")

# ==========================
# Database giả
# ==========================

tickets_db = [
    {
        "id": 1,
        "movie_name": "Doctor Strange 3",
        "room_code": "IMAX-01",
        "quantity": 2,
        "status": "confirmed",
        "created_at": "2026-07-01T19:00:00Z",
    },
    {
        "id": 2,
        "movie_name": "Avatar 3",
        "room_code": "PREMIUM-02",
        "quantity": 1,
        "status": "confirmed",
        "created_at": "2026-07-01T20:15:00Z",
    },
]


# ==========================
# Schema
# ==========================

class TicketCreate(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=10)


# ==========================
# Hàm tạo timestamp
# ==========================

def current_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ==========================
# Unified Response
# ==========================

def response(
    request: Request,
    status_code: int,
    message: str,
    data=None,
    error=None,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "data": data,
            "error": error,
            "timestamp": current_time(),
            "path": request.url.path,
        },
    )


# ==========================
# Exception HTTP
# ==========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return response(
        request=request,
        status_code=exc.status_code,
        message=exc.detail["message"],
        data=None,
        error=exc.detail["error"],
    )


# ==========================
# Exception Validation 422
# ==========================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return response(
        request=request,
        status_code=422,
        message="Lỗi: Dữ liệu đầu vào không hợp lệ!",
        data=None,
        error=exc.errors(),
    )


# ==========================
# GET /tickets
# ==========================

@app.get("/tickets")
def get_tickets(request: Request):
    return response(
        request=request,
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách vé thành công!",
        data=tickets_db,
    )


# ==========================
# POST /tickets
# ==========================

@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate, request: Request):

    # Kiểm tra trùng movie + room
    for item in tickets_db:
        if (
            item["movie_name"].lower() == ticket.movie_name.lower()
            and item["room_code"].lower() == ticket.room_code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!",
                    "error": "ERR-CINE-01: Ticket conflict for movie and room combination.",
                },
            )

    # Sinh ID mới
    if tickets_db:
        new_id = max(ticket["id"] for ticket in tickets_db) + 1
    else:
        new_id = 1

    new_ticket = {
        "id": new_id,
        "movie_name": ticket.movie_name,
        "room_code": ticket.room_code,
        "quantity": ticket.quantity,
        "status": "confirmed",
        "created_at": current_time(),
    }

    tickets_db.append(new_ticket)

    return response(
        request=request,
        status_code=status.HTTP_201_CREATED,
        message="Đặt vé thành công!",
        data=new_ticket,
    )


# ==========================
# DELETE /tickets/{ticket_id}
# ==========================

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, request: Request):

    for ticket in tickets_db:
        if ticket["id"] == ticket_id:
            tickets_db.remove(ticket)

            return response(
                request=request,
                status_code=status.HTTP_200_OK,
                message="Hủy vé thành công!",
                data=None,
            )

    raise HTTPException(
        status_code=404,
        detail={
            "message": "Lỗi: Không tìm thấy mã vé yêu cầu!",
            "error": "ERR-CINE-02: Ticket ID does not exist.",
        },
    )