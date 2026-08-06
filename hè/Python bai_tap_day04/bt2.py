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

def safe_process_invoice(order_id, raw_total, discount_code, is_vip):

    try:

        total = float(raw_total)

        if discount_code == "VIP10":
            discount = total * 0.1

        elif discount_code == "VIP20":
            discount = total * 0.2

        else:
            discount = 0

        after_discount = total - discount

        vat = after_discount * 0.1

        final = after_discount + vat
        if is_vip and total >= 10000000:
            category = "HÓA ĐƠN LỚN (VIP)"
        else:
            category = "HÓA ĐƠN THƯỜNG"

        print(
            f"[{order_id}] Tiền hàng: {total:,.0f} | "
            f"CK: {discount:,.0f} | "
            f"VAT 10%: {vat:,.0f} | "
            f"Tổng: {final:,.0f} VNĐ "
            f"[{category}]"
        )

    except ValueError:
        print(f"Xử lý lỗi [{order_id}]: Số tiền '{raw_total}' không hợp lệ! Bỏ qua đơn hàng.")

print("\nBÁO CÁO XỬ LÝ HÓA ĐƠN AN TOÀN")

for order in orders:

    safe_process_invoice(
        order["id"],
        order["total"],
        order["discount_code"],
        order["is_vip"]
    )