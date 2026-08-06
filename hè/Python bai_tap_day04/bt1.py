# Dataset raw_registers & orders:
raw_registers = [
    {"name": "  Nguyen Van An  ", "email": "an.nguyen@gmail.com", "phone": "0987654321"},
    {"name": "Tran Thi Bich", "email": "bich_gmail.com", "phone": "0912345678"},
    {"name": "Le Hoang Cuong", "email": "cuong@rikkei.edu.vn", "phone": "0123456789"},
    {"name": "  Pham Minh Dung ", "email": "dung@gmail.com  ", "phone": "0355667788"}
]

orders = [
    {"id": "DH01", "total": "12500000", "discount_code": "VIP10", "is_vip": True},
    {"id": "DH02", "total": "450000", "discount_code": "INVALID", "is_vip": False},
    {"id": "DH03", "total": "ABC_ERROR", "discount_code": "", "is_vip": False},
    {"id": "DH04", "total": "8500000", "discount_code": "VIP20", "is_vip": True}
]

def validate_registration_input(name, email, phone):
    clean_name = name.strip()
    clean_email = email.strip().lower()
    clean_phone = phone.strip()

    ok_email = "@" in clean_email

    valid_phone = ("03", "05", "07", "08", "09")
    ok_phone = (
        len(clean_phone) == 10
        and clean_phone.isdigit()
        and clean_phone.startswith(valid_phone)
    )

    return clean_name, clean_email, ok_email, clean_phone, ok_phone

print("BÁO CÁO CHUẨN HÓA & VALIDATE THÔNG TIN ĐĂNG KÝ")

stt = 1

for student in raw_registers:

    result = validate_registration_input(
        student["name"],
        student["email"],
        student["phone"]
    )

    name = result[0]
    email = result[1]
    ok_email = result[2]
    phone = result[3]
    ok_phone = result[4]

    if ok_email and ok_phone:
        print(f"[{stt}] {name} | Email: {email} | SĐT: {phone} -> HỢP LỆ")

    elif not ok_email:
        print(f"[{stt}] {name} | Email: {email} | SĐT: {phone} -> KHÔNG HỢP LỆ (Thiếu '@')")

    else:
        print(f"[{stt}] {name} | Email: {email} | SĐT: {phone} -> KHÔNG HỢP LỆ (Sai đầu số VN)")

    stt += 1