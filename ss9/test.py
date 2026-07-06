from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Cinema Ticket Booking API")
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


class TicketCreate(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=10)


def current_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

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

@app.get("/tickets")
def get_tickets(request: Request):
    return response(
        request=request,
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách vé thành công!",
        data=tickets_db,
    )

@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate, request: Request):

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