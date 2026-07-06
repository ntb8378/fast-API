from fastapi import FastAPI, Request,HTTPException,status
from pydantic import BaseModel,Field
from typing import Any,Optional
from datetime import timezone, datetime,UTC
from fastapi.responses import JSONResponse

app = FastAPI(
title = "Cinema ticket booking API",
description = "API hệ thống Đặt ve xem phim online"

)

class TicketRequestDTO(BaseModel):
    movie_name: str = Field(...)
    room_code: str = Field(...)
    quantity: int = Field(..., ge=1, le=10)

class APIRespone(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str

def success_respone(statusCode: int, message:str, data:Any, error:Any):
    return APIRespone(
        statusCode= statusCode,
        message = message,
        data = data,
        error = error,
        timestamp = datetime.now(timezone.utc).isoformat,
        path = Request.url.path
    )

@app.exception_handler(HTTPException)
def http_exception_handler(exc: HTTPException):
    return JSONResponse(
        status_code = 404,
        content = APIResponse(
        statusCode = exc. status_code,
        message = exc.detail,
        data = None,
        timestamp = datetime.now(timezone.utc).isoformat(),
        path = request.url.path
    ).model_dump()

)

tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed", "created_at": "2026-07-01T19:00:00Z"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed", "created_at": "2026-07-01T20:15:00Z"}
]

@app.get("/tickets", tags=["Tickets"], status_code= status.HTTP_200_OK)
def get_tickets():
    if not tickets_db:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return success_respone(200, "lấy dữ liệu thành công", tickets_db, None, Request)