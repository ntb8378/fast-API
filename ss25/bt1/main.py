import uuid
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_COURSES = [
    "Python Basic",
    "FastAPI",
    "Data Analysis",
]

# Giới hạn 2 MB = 2 * 1024 * 1024 bytes
MAX_FILE_SIZE = 2097152
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]


@app.post("/students/register")
async def register_student(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    course: str = Form(...),
    avatar: UploadFile = File(...),
):
    # 1. Kiểm tra Họ và Tên (dùng strip)
    clean_name = full_name.strip()
    if not clean_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Họ và tên không được để trống",
        )

    # 2. Kiểm tra Email cơ bản
    if "@" not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email không hợp lệ"
        )

    # 3. Kiểm tra số điện thoại (đúng 10 chữ số)
    if len(phone) != 10 or not phone.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số điện thoại phải gồm đúng 10 chữ số",
        )

    # 4. Kiểm tra khóa học
    if course not in ALLOWED_COURSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Khóa học không hợp lệ"
        )

    # 5. Kiểm tra định dạng ảnh (chỉ JPG, PNG)
    if avatar.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ảnh đại diện chỉ chấp nhận định dạng JPG hoặc PNG",
        )

    # 6. Đọc nội dung và kiểm tra kích thước (< 2 MB)
    content = await avatar.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Kích thước ảnh không được vượt quá 2 MB",
        )

    # 7. Sinh tên file mới chống trùng lặp và ghi đè
    # Lấy đuôi file từ tên file gốc (nếu có), mặc định là png
    file_ext = avatar.filename.split(".")[-1] if "." in avatar.filename else "png"
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # Chỉ ghi file khi mọi điều kiện (1 -> 6) đã vượt qua
    with open(file_path, "wb") as file:
        file.write(content)

    return {
        "success": True,
        "message": "Đăng ký thành công",
        "data": {
            "full_name": clean_name,
            "email": email,
            "phone": phone,
            "course": course,
            "avatar": str(file_path),
        },
    }
