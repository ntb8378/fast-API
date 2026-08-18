from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer


# ==========================================
# 1. KHỞI TẠO FASTAPI
# ==========================================

app = FastAPI()


# ==========================================
# 2. CẤU HÌNH CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 3. OAUTH2
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ==========================================
# 4. DỮ LIỆU TOKEN GIẢ LẬP
# ==========================================

TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },

    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },

    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}


# ==========================================
# 5. MIDDLEWARE XÁC THỰC
# ==========================================

@app.middleware("http")
async def authentication_middleware(request, call_next):

    # /health được phép truy cập công khai
    if request.url.path == "/health":
        response = await call_next(request)
        response.headers["X-System-Name"] = (
            "Learning Management System"
        )
        return response

    # OPTIONS là CORS preflight
    # Không được yêu cầu JWT
    if request.method == "OPTIONS":
        response = await call_next(request)
        response.headers["X-System-Name"] = (
            "Learning Management System"
        )
        return response

    # Các request còn lại phải có Authorization
    if "authorization" not in request.headers:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Authorization header is required"
            },
        )

    response = await call_next(request)

    # Thêm header hệ thống
    response.headers["X-System-Name"] = (
        "Learning Management System"
    )

    return response


# ==========================================
# 6. LẤY USER HIỆN TẠI
# ==========================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    user = TOKENS.get(token)

    # Token không tồn tại
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    # Tài khoản bị khóa
    if not user["is_active"]:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive",
        )

    return user


# ==========================================
# 7. KIỂM TRA QUYỀN ADMIN
# ==========================================

def require_admin(
    current_user: dict = Depends(get_current_user)
):
    # Chỉ admin mới được phép
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required",
        )

    return current_user


# ==========================================
# 8. HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():
    return {
        "status": "UP"
    }


# ==========================================
# 9. XEM DANH SÁCH KHÓA HỌC
# ==========================================

@app.get("/courses")
def get_courses(
    current_user: dict = Depends(get_current_user)
):
    return {
        "items": [
            {
                "id": 1,
                "name": "FastAPI Basic"
            },
            {
                "id": 2,
                "name": "FastAPI Security"
            },
        ]
    }


# ==========================================
# 10. XÓA KHÓA HỌC - CHỈ ADMIN
# ==========================================

@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin),
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }