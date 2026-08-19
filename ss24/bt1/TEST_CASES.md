# 3. Kịch Bản Kiểm Thử (Test Cases)

Bạn có thể sử dụng terminal (Lệnh `curl` + \` ) hoặc phần mềm Postman để thực thi các kịch bản sau nhằm xác minh tính chính xác của hệ thống. Trước khi test, hãy chạy ứng dụng bằng lệnh: `uvicorn main:app --reload` (Server sẽ chạy ở cổng `8000`).

---

## Test 1: Kiểm thử Phân quyền (RBAC)

### Trường hợp 1 (Nhân viên STAFF cố gắng truy cập cài đặt hệ thống):

- Lệnh: 

```json
curl -H "X-User-Role: STAFF" http://localhost:8000/api/v1/system/settings
```

- Kết quả mong đợi: Mã lỗi 403 Forbidden và trả về 

```json
{"error": "Permission Denied"}.
```

### Trường hợp 2 (Quản trị viên ADMIN truy cập cài đặt hệ thống):

- Lệnh: 
```json
curl -H "X-User-Role: ADMIN" http://localhost:8000/api/v1/system/settings
```

- Kết quả mong đợi: Mã 200 OK và trả về 
```json
{"message": "Success! You have accessed system settings."}.
```

## Test 2: Kiểm thử cấu hình CORS

Để kiểm tra `CORS`, chúng ta sẽ giả lập một request gửi từ domain độc hại (`evil-attacker.xyz`) để xem `Backend` có từ chối cấp quyền hay không (thông qua cơ chế preflight request `OPTIONS` của `CORS`).
---

### Trường hợp gửi từ Origin không hợp lệ:

- Lệnh: 

```json
curl -X OPTIONS -H "Origin: [https://evil-attacker.xyz](https://evil-attacker.xyz)" -H "Access-Control-Request-Method: GET" -v http://localhost:8000/api/v1/profile
```

- Kết quả mong đợi: Trong log trả về của curl, bạn sẽ không thấy sự xuất hiện của Header 
```json
Access-Control-Allow-Origin: [https://evil-attacker.xyz](https://evil-attacker.xyz)
```
Trình duyệt của nạn nhân sẽ tự động chặn request này vì domain không khớp với danh sách được phép.

#### Trường hợp gửi từ Origin hợp lệ (Frontend của MegaMart):

- Lệnh: 
```json
curl -X OPTIONS -H "Origin: [https://internal.megamart.com](https://internal.megamart.com)" -H "Access-Control-Request-Method: GET" -v http://localhost:8000/api/v1/profile
```

- Kết quả mong đợi: Server trả về Header 
```json
Access-Control-Allow-Origin: [https://internal.megamart.com](https://internal.megamart.com), cho phép trình duyệt tiếp tục gửi request thực sự.
```