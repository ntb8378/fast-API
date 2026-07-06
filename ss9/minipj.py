from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime, timezone

app = FastAPI(version="1.0")


# ================= DATABASE =================

tasks_db = [
    {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]


# ================= SCHEMA =================

class TaskCreateSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=1)
    assignee: str = Field(min_length=1)
    priority: int = Field(ge=1, le=5)

    @field_validator("assignee")
    @classmethod
    def validate_assignee(cls, value):
        return value.strip()


class TaskStatusUpdateSchema(BaseModel):
    status: Literal["todo", "in_progress", "done"]


# ================= RESPONSE =================

def create_response(
        status_code: int,
        message: str,
        data=None,
        error=None,
        path: str = ""
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "path": path
    }


# ================= EXCEPTION =================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=create_response(
            422,
            "Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
            None,
            "ERR-VAL-422: Validation error at Request Body fields constraint layout.",
            request.url.path
        )
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=create_response(
            500,
            "Lỗi hệ thống!",
            None,
            "ERR-500: Internal Server Error.",
            request.url.path
        )
    )


# ================= FUNCTION =================

def calculate_team_metrics():

    total_tasks = len(tasks_db)

    completed_tasks = sum(
        1 for task in tasks_db
        if task["status"] == "done"
    )

    completion_rate = 0

    if total_tasks != 0:
        completion_rate = round(
            completed_tasks / total_tasks * 100,
            2
        )

    return (
        total_tasks,
        completed_tasks,
        completion_rate
    )


# ================= API =================

# Chức năng 1
@app.get("/tasks")
def get_all_tasks(request: Request, status: Optional[str] = None):

    if status:
        result = [
            task for task in tasks_db
            if task["status"] == status
        ]
    else:
        result = tasks_db

    return create_response(
        200,
        "Lấy danh sách công việc thành công!",
        result,
        None,
        request.url.path
    )


# Chức năng 2
@app.post("/tasks", status_code=201)
def create_task(task_in: TaskCreateSchema, request: Request):

    for task in tasks_db:
        if task["title"] == task_in.title:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                    "error": "ERR-TASK-01: Task conflict: Title field duplicates an existing record."
                }
            )

    new_id = max(task["id"] for task in tasks_db) + 1 if tasks_db else 1

    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee,
        "priority": task_in.priority,
        "status": "todo",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    tasks_db.append(new_task)

    return create_response(
        201,
        "Khởi tạo công việc mới thành công!",
        new_task,
        None,
        request.url.path
    )


# Chức năng 3
@app.put("/tasks/{task_id}")
def update_task_status(
        task_id: int,
        status_in: TaskStatusUpdateSchema,
        request: Request
):

    for task in tasks_db:

        if task["id"] == task_id:

            if task["status"] == "done":
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": "Lỗi: Công việc đã hoàn thành, không thể cập nhật!",
                        "error": "ERR-TASK-04: Completed task cannot be updated."
                    }
                )

            task["status"] = status_in.status

            return create_response(
                200,
                "Cập nhật tiến độ công việc thành công!",
                task,
                None,
                request.url.path
            )

    raise HTTPException(
        status_code=404,
        detail={
            "message": "Lỗi: Không tìm thấy công việc!",
            "error": "ERR-TASK-03: Task not found."
        }
    )


# Chức năng 4
@app.get("/tasks/analytics/dashboard")
def get_dashboard_analytics(request: Request):

    total, completed, rate = calculate_team_metrics()

    return create_response(
        200,
        "Lấy số liệu thống kê hiệu suất nhóm thành công!",
        {
            "total_tasks": total,
            "completed_tasks": completed,
            "completion_rate_percentage": rate
        },
        None,
        request.url.path
    )


# ================= HTTP EXCEPTION =================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    detail = exc.detail

    if isinstance(detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=create_response(
                exc.status_code,
                detail["message"],
                None,
                detail["error"],
                request.url.path
            )
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(
            exc.status_code,
            str(detail),
            None,
            str(detail),
            request.url.path
        )
    )