
# Phần 1: Phát hiện lỗi và Test case

## 1. Phân tích các đoạn code chưa đúng
- Thiếu hàm `strip()`: Kiểm tra `if full_name == ""` chỉ chặn được chuỗi rỗng hoàn toàn, không chặn được trường hợp người dùng nhập toàn dấu cách (khoảng trắng).

- Bỏ sót kiểm tra Email: Mã nguồn hoàn toàn không có đoạn code nào kiểm tra sự tồn tại của ký tự `@` trong biến `email`.

- Sai logic số điện thoại: Logic `if len(phone) < 10` cho phép số điện thoại có 11, 12 số, đồng thời không ngăn chặn việc nhập chữ cái (ví dụ: `abc`).

- Thiếu kiểm tra định dạng và kích thước File: Không có đoạn code nào đọc `content_type` để giới hạn định dạng (JPG, PNG) và không đo lường dung lượng file trước khi lưu, dẫn đến rủi ro tràn ổ cứng.

- Ghi đè file: Việc dùng trực tiếp `avatar.filename` từ người dùng (`file_path = UPLOAD_DIR / avatar.filename`) sẽ khiến các file có cùng tên bị ghi đè lên nhau.

- Trả về sai HTTP Status Code: Khi có lỗi, code đang trả về một JSON báo lỗi nhưng HTTP Status Code ngầm định vẫn là 200 OK. Điều này sai chuẩn RESTful API, cần dùng 400 Bad Request hoặc 413 Payload Too Large.

## 2. Danh sách 5 Test Cases

### Test case 1: Họ tên chỉ chứa khoảng trắng

- Dữ liệu đầu vào: `full_name = "   "`

- Kết quả hiện tại: 200 OK (Vẫn lưu thành công).

- Kết quả mong đợi: 400 Bad Request.

- Nguyên nhân sai: Do không dùng hàm `.strip()` để loại bỏ khoảng trắng thừa trước khi so sánh.

### Test case 2: Số điện thoại chứa chữ và sai độ dài

- Dữ liệu đầu vào: `phone = "09876abcde"`

- Kết quả hiện tại: 200 OK.

- Kết quả mong đợi: 400 Bad Request.

- Nguyên nhân sai: Độ dài chuỗi là 10 (không bị chặn bởi `< 10`) và không có hàm `isdigit()` để xác tra tính dạng số.

### Test case 3: Upload tài liệu PDF

- Dữ liệu đầu vào: `avatar = student-profile.pdf`

- Kết quả hiện tại: 200 OK (File PDF được lưu vào máy chủ).

- Kết quả mong đợi: 400 Bad Request.

- Nguyên nhân sai: Không kiểm tra `content_type` của file gửi lên.

### Test case 4: Upload ảnh lớn hơn 2 MB

- Dữ liệu đầu vào: `avatar = high-res-photo.png` (Kích thước: 5 MB).

- Kết quả hiện tại: 200 OK.

- Kết quả mong đợi: 413 Payload Too Large.

- Nguyên nhân sai: Backend đọc và ghi thẳng dữ liệu ra đĩa mà không đo lường dung lượng bộ nhớ.

### Test case 5: Hai sinh viên upload file cùng tên

- Dữ liệu đầu vào: Sinh viên A upload `avatar.jpg`. Sinh viên B cũng upload `avatar.jpg`.

- Kết quả hiện tại: File của sinh viên B ghi đè lên file của sinh viên A.

- Kết quả mong đợi: Hai file được cấp tên riêng biệt, tồn tại song song.

- Nguyên nhân sai: Tin tưởng tuyệt đối và dùng lại nguyên bản tên file do client gửi lên.

# Phần 2: Sửa Source Code
> Đọc main.py