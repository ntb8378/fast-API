import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


SECRET_KEY = "my-super-secret-key"
ALGORITHM = "HS256"


# 1. Tạo Access Token
def create_access_token(data: dict, expires_minutes: int) -> str:

    # Copy dữ liệu để tạo Payload
    to_encode = data.copy()

    # Lấy thời gian hiện tại
    now = datetime.now(timezone.utc)

    # Tính thời gian hết hạn
    expire = now + timedelta(minutes=expires_minutes)

    # Thêm thời gian hết hạn vào Payload
    to_encode.update({"exp": expire})

    # Tạo JWT bằng Payload + SECRET_KEY + HS256
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# 2. Kiểm tra và giải mã Access Token
def decode_access_token(token: str) -> dict:

    try:
        # Kiểm tra Signature và thời gian hết hạn
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except ExpiredSignatureError:
        raise ValueError("Token đã hết hạn")

    except InvalidTokenError:
        raise ValueError("Token không hợp lệ")


# 3. Tạo Token
token = create_access_token(
    data={
        "sub": "student01@gmail.com",
        "user_id": 1,
        "role": "student"
    },
    expires_minutes=30
)


# 4. In Token
print("Access Token:")
print(token)


# 5. Giải mã và kiểm tra Token
print("\nPayload:")
print(decode_access_token(token))