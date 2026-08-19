from fastapi import FastAPI, Header, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="FlashMove Logistics API")

# ==========================================
# CẤU HÌNH CORS MULTI-ORIGIN WHITELIST
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://driver.flashmove.io", "https://hub.flashmove.io"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "X-Role-Identity"],
)


# ==========================================
# MIDDLEWARE XÁC THỰC QUYỀN HẠN (RBAC)
# ==========================================
class AuthorizationException(Exception):
    pass


@app.exception_handler(AuthorizationException)
async def auth_exception_handler(request: Request, exc: AuthorizationException):
    return JSONResponse(
        status_code=403,
        content={"status": "Rejected", "reason": "Unauthorized action for this role"},
    )


def require_roles(allowed_roles: list[str]):
    def role_checker(x_role_identity: str = Header(default=None)):
        # Kiểm tra nếu Header trống hoặc Role không hợp lệ
        if not x_role_identity or x_role_identity not in allowed_roles:
            raise AuthorizationException()
        return x_role_identity

    return role_checker


# ==========================================
# THIẾT LẬP API ENDPOINTS THỰC NGHIỆM
# ==========================================
@app.post(
    "/api/v1/orders/assign", dependencies=[Depends(require_roles(["DISPATCHER"]))]
)
def assign_order():
    return {"message": "Order assigned successfully."}


@app.patch(
    "/api/v1/orders/status",
    dependencies=[Depends(require_roles(["DISPATCHER", "DRIVER"]))],
)
def update_order_status():
    return {"message": "Order status updated successfully."}


@app.get(
    "/api/v1/orders/track",
    dependencies=[Depends(require_roles(["DISPATCHER", "DRIVER", "CUSTOMER_SUPPORT"]))],
)
def track_order():
    return {"message": "Order tracking details."}
