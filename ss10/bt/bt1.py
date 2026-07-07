# STT 1
# Hành vi lỗi:
# - Thiếu lệnh db.commit() sau db.add(new_product).
#
# Hậu quả:
# - Dữ liệu chỉ được thêm vào Session, không được lưu vĩnh viễn vào bảng products trong MySQL.
# - API vẫn trả về thành công nhưng database không có bản ghi mới.
#
# Cách khắc phục:
# - Gọi db.commit() sau db.add(new_product) để xác nhận transaction và ghi dữ liệu xuống database.

# STT 2
# Hành vi lỗi:
# - Không đóng Session sau khi xử lý (thiếu db.close()).
#
# Hậu quả:
# - Kết nối MySQL không được giải phóng, dễ gây rò rỉ kết nối (connection leak).
# - Nhiều request liên tiếp có thể làm cạn connection pool và ảnh hưởng hiệu năng.
#
# Cách khắc phục:
# - Gọi db.close() sau khi xử lý (nên đặt trong khối finally) để luôn giải phóng kết nối.