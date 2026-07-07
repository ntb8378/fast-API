# STT 1
# Phương thức truy vấn hiện tại:
# - .one()
#
# Tình huống gây lỗi (Edge Case):
# - order_id = 999 không tồn tại trong database.
# - .one() sẽ phát sinh ngoại lệ (NoResultFound), nếu không xử lý sẽ trả về HTTP 500 và lộ Stack Trace.
#
# Phương thức thay thế an toàn hơn:
# - Sử dụng .first() để trả về None nếu không tìm thấy dữ liệu.
# - Kiểm tra nếu order is None thì raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found").