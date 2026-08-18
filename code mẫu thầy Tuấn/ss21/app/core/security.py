import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

# Cấu hình JWT (JSON Web Token)
SECRET_KEY = "your-super-secret-key-for-jwt-do-not-share" # Khóa bí mật dùng để ký token
ALGORITHM = "HS256" # Thuật toán mã hóa
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Thời gian sống của token (ví dụ: 60 phút)

def hash_password(password: str, cost_factor: int = 12) -> str:
    """
    Băm mật khẩu sử dụng thư viện bcrypt trực tiếp.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=cost_factor)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Kiểm tra mật khẩu người dùng nhập vào có khớp với mật khẩu đã băm trong DB hay không.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    """
    Tạo Access Token (JWT) dựa trên thông tin payload (data) được truyền vào.
    """
    to_encode = data.copy()
    
    # Tính toán thời gian hết hạn (expiration time)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Ký và tạo token chuỗi token bằng thư viện PyJWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
