# Phần 1. Phát hiện lỗi

Trong đoạn code hiện tại có rất nhiều lỗ hổng và thiếu sót về mặt logic, cụ thể gồm 8 lỗi chính như sau:

1. Cách lấy phần mở rộng file (File Extension) sai logic:

    - Code cũ dùng `document.filename.split(".")[1]`.

    - Hậu quả: Nếu file tên là `baitap.pdf.exe`, đuôi lấy được sẽ là `pdf` thay vì `exe`, khiến hệ thống bị lọt file thực thi (bypass extension check). Nếu file không có đuôi (như `README`), sẽ gây lỗi `IndexError` làm sập API.

2. Không tạo thư mục lưu trữ:

    - Không có lệnh kiểm tra hay khởi tạo thư mục `storage/documents`.

    - Hậu quả: Nếu server chạy ở môi trường mới chưa có sẵn thư mục này, API sẽ bị crash (lỗi `FileNotFoundError`) khi cố gắng lưu file.

3. Không kiểm tra file rỗng:

    - Code đọc và ghi file ngay lập tức mà không kiểm tra số lượng byte.

    - Hậu quả: File 0 byte vẫn được lưu lên server, gây rác dữ liệu.

4. Không kiểm tra kích thước file (Size Limit):

    - Bỏ qua việc giới hạn dung lượng file gửi lên.

    - Hậu quả: Người dùng có thể upload file hàng chục GB, dẫn đến đầy bộ nhớ máy chủ (Disk Full) hoặc từ chối dịch vụ (DoS).

5. Không chuẩn hóa mã môn học và tiêu đề rỗng:

    - Biến `course_code` không được `upper()`, và biến `title` không được chặn chuỗi rỗng/khoảng trắng.

    - Hậu quả: Dữ liệu lưu xuống database không đồng nhất (`IT215` khác `it215`), hoặc tài liệu không có tên nhưng vẫn tồn tại.

6. Không kiểm tra loại tài liệu (`document_type`):

    - Biến `document_type` nhận vào bất cứ chuỗi nào người dùng truyền lên.

    - Hậu quả: Giá trị này rác, không tuân theo danh mục hợp lệ (`lecture`, `assignment`, `reference`).

7. Nguy cơ ghi đè file (File Overwrite Risk):

    - Code cũ sử dụng nguyên `document.filename` để lưu trên server.

    - Hậu quả: Hai sinh viên cùng upload file `baitap.pdf` thì người tải lên sau sẽ xóa vĩnh viễn file của người trước.

8. Nguy cơ sử dụng tên file không an toàn (Path Traversal Risk):

    - Sử dụng trực tiếp tên người dùng đưa lên mà không làm sạch.

    - Hậu quả: Hacker có thể gửi file có tên `../../../etc/passwd` nhằm ghi đè các file cấu hình hệ thống quan trọng.

# Phần 2. Sửa Source Code
> Đọc main.py