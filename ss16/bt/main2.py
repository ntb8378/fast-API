from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class UserProfileCreate(BaseModel):
    full_name: str
    phone: str
    address: str | None = None

users = [
    {
        "id": 1,
        "username": "nguyenvanan",
        "email": "an@gmail.com"
    },
    {
        "id": 2,
        "username": "tranthibinh",
        "email": "binh@gmail.com"
    }
]

profiles = [
    {
        "id": 10,
        "full_name": "Nguyễn Văn An",
        "phone": "0901000001",
        "address": "Hà Nội",
        "user_id": 1
    }
]

@app.get("/users")
def get_users():
    return users

@app.get("/profiles")
def get_profiles():
    return profiles

@app.post(
    "/users/{user_id}/profile",
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    user_id: int,
    profile_data: UserProfileCreate
):
    # 1. KIỂM TRA NGƯỜI DÙNG TỒN TẠI (Bổ sung mới)
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )

    # 2. KIỂM TRA NGƯỜI DÙNG ĐÃ CÓ HỒ SƠ (Sửa lỗi logic: đối chiếu bằng user_id thay vì id)
    existing_profile = next(
        (
            profile
            for profile in profiles
            if profile["user_id"] == user_id
        ),
        None
    )
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Người dùng đã có hồ sơ"
        )

    # 3. KIỂM TRA TRÙNG SỐ ĐIỆN THOẠI TOÀN HỆ THỐNG (Sửa lỗi logic: loại bỏ vế so sánh user_id)
    duplicated_phone = next(
        (
            profile
            for profile in profiles
            if profile["phone"] == profile_data.phone
        ),
        None
    )
    if duplicated_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Số điện thoại đã được sử dụng"
        )

    # 4. TẠO HỒ SƠ MỚI
    new_profile = {
        "id": len(profiles) + 10,  # Sinh mã hồ sơ mới đảm bảo phân biệt
        "full_name": profile_data.full_name,
        "phone": profile_data.phone,
        "address": profile_data.address,
        "user_id": user_id
    }
    profiles.append(new_profile)
    return new_profile