from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="MegaMart ERP Backend")

# ==========================================
# PHẦN 4: CẤU HÌNH CORS NGHIÊM NGẶT
# ==========================================
# Ràng buộc:
# 1. Không dùng "*"
# 2. Chỉ cho phép https://internal.megamart.com
# 3. Chỉ cho phép GET, POST
# 4. Chỉ cho phép Headers: Content-Type, X-User-Role
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://internal.megamart.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-User-Role"],
)


# ==========================================
# PHẦN 1 & 2: HỆ THỐNG VAI TRÒ VÀ MIDDLEWARE
# ==========================================


# Tạo một Custom Exception để dễ dàng trả về JSON format như yêu cầu
class PermissionDeniedException(Exception):
    pass


@app.exception_handler(PermissionDeniedException)
async def permission_denied_handler(request: Request, exc: PermissionDeniedException):
    # Trả về đúng mã 403 và format {"error": "Permission Denied"}
    return JSONResponse(
        status_code=403,
        content={"error": "Permission Denied"},
    )


# Dependency đóng vai trò như Middleware kiểm tra phân quyền
def role_required(allowed_roles: list[str]):
    def role_checker(x_user_role: str = Header(default=None)):
        if not x_user_role or x_user_role not in allowed_roles:
            raise PermissionDeniedException()
        return x_user_role

    return role_checker


# ==========================================
# PHẦN 3: XÂY DỰNG API ENDPOINT THỬ NGHIỆM
# ==========================================
from fastapi import Depends


@app.get(
    "/api/v1/salary/modify", dependencies=[Depends(role_required(["ADMIN", "HR"]))]
)
def modify_salary():
    return {"message": "Success! You have access to modify salary."}


@app.get("/api/v1/system/settings", dependencies=[Depends(role_required(["ADMIN"]))])
def system_settings():
    return {"message": "Success! You have accessed system settings."}


@app.get(
    "/api/v1/profile", dependencies=[Depends(role_required(["ADMIN", "HR", "STAFF"]))]
)
def get_profile():
    return {"message": "Success! You have accessed your profile."}


# Lệnh chạy server (dùng cho terminal):
# uvicorn main:app --reload
