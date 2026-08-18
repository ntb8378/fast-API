from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


# =========================
# 1. CẤU HÌNH
# =========================

app = FastAPI()

SECRET_KEY = "training-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================
# 2. DỮ LIỆU USER GIẢ LẬP
# =========================

USERS = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Nguyen",
        "role": "user",
        "is_active": True,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Tran",
        "role": "user",
        "is_active": False,
    },
}


# =========================
# 3. TẠO TOKEN ĐỂ TEST
# =========================

@app.get("/issue-token/{username}")
def issue_token(username: str, expired: bool = False):

    # Kiểm tra username có tồn tại không
    if username not in USERS:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Tạo thời gian hết hạn
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=-5 if expired else 30
    )

    # Tạo JWT
    token = jwt.encode(
        {
            "sub": username,
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# =========================
# 4. CURRENT USER DEPENDENCY
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        # Kiểm tra chữ ký và thời hạn của JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except Exception:
        # Token không hợp lệ hoặc đã hết hạn
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # Lấy username từ claim "sub"
    username = payload.get("sub")

    # Token không có sub
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # Tìm user trong hệ thống
    user = USERS.get(username)

    # User không tồn tại
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Kiểm tra tài khoản có đang hoạt động không
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    # Tất cả kiểm tra đều hợp lệ
    return user


# =========================
# 5. GET CURRENT USER
# =========================

@app.get("/users/me")
def read_current_user(
    current_user: dict = Depends(get_current_user)
):
    return current_user