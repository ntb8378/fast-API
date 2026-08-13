from datetime import datetime, timezone
from typing import Any, Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    path: str


def response_format(
    request: Request,
    status_code: int,
    message: str,
    data: Optional[Any] = None,
    error: Optional[Any] = None,
) -> JSONResponse:
    payload = {
        "statusCode": status_code,
        "message": message,
        "data": (
            data
            if data is not None
            else ([] if isinstance(data, list) else {} if status_code < 400 else None)
        ),
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "path": request.url.path,
    }
    return JSONResponse(status_code=status_code, content=payload)
