students = [
    {
        "id": "SV01",
        "name": " Nguyen Van An ",
        "email": "an.nguyen@rikkei.edu.vn ",
        "phone": " 0987654321 ",
    },
    {
        "id": "SV02",
        "name": "Tran Thi Bich",
        "email": "bich_gmail.com",
        "phone": "0912345678",
    },
    {
        "id": "SV03",
        "name": "Le Hoang Cuong",
        "email": "cuong@gmail.com",
        "phone": "09876abcde",
    },
    {
        "id": "SV04",
        "name": "Pham Minh Dung",
        "email": "dung@gmail.com",
        "phone": "0355667788",
    },
]

def validate_student_info(email, phone):
    clean_email = email.strip()
    clean_phone = phone.strip()

    # Kiểm tra Email
    if clean_email.count("@") != 1:
        return (
            clean_email,
            clean_phone,
            False,
            "Thieu @" if clean_email.count("@") == 0 else "Du ky tu @",
        )
    if not (clean_email.endswith(".com") or clean_email.endswith(".edu.vn")):
        return clean_email, clean_phone, False, "Sai ten mien"

    # Kiểm tra SĐT
    if not clean_phone.isdigit():
        return clean_email, clean_phone, False, "SDT chua chu"
    if len(clean_phone) != 10:
        return clean_email, clean_phone, False, "SDT khong du 10 so"
    if not clean_phone.startswith("0"):
        return clean_email, clean_phone, False, "SDT khong bat dau bang 0"

    return clean_email, clean_phone, True, "HO SO HOP LE"


# 2. Duyệt qua từng sinh viên và in kết quả
for sv in students:
    sv_id = sv["id"].strip()
    clean_name = sv["name"].strip()

    c_email, c_phone, is_valid, status_msg = validate_student_info(
        sv["email"], sv["phone"]
    )

    if is_valid:
        print(
            f"[{sv_id}] {clean_name} | Email: {c_email} | SDT: {c_phone} -> HO SO HOP LE"
        )
    else:
        print(
            f"[{sv_id}] {clean_name} | Email: {c_email} | SDT: {c_phone} -> KHONG HOP LE ({status_msg})"
        )
