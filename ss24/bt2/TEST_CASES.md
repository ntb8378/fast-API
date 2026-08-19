# Yêu Cầu 3: Kịch Bản Kiểm Thử (Test Cases)


### Để chạy server, bạn hãy dùng lệnh `uvicorn main:app --reload` (Mặc định chạy ở cổng `8000`). Sau đó dùng `curl` hoặc `Postman` để kiểm thử.

---

## Kịch bản 1 (Chặn quyền - Lỗi 403):

#### Lệnh: 
```json
curl -X POST -H "X-Role-Identity: DRIVER" http://localhost:8000/api/v1/orders/assign
```
#### Kết quả: Hệ thống chặn và trả về lỗi 403 `Forbidden` với `JSON` 

```json
{"status": "Rejected", "reason": "Unauthorized action for this role"}.
```
## Kịch bản 2 (Duyệt quyền - `200 OK`):

#### Lệnh: 
```json
curl -X POST -H "X-Role-Identity: DISPATCHER" http://localhost:8000/api/v1/orders/assign
```
#### Kết quả: Hệ thống cấp phép truy cập, trả về `HTTP 200 OK` và `JSON` 

```json
{"message": "Order assigned successfully."}.
```

## Kịch bản 3 (`CORS Domain` Lạ - Bị từ chối):

#### Lệnh (Gửi Preflight Request):

```json
 curl -X OPTIONS -H "Origin: [https://evil-competitor.com](https://evil-competitor.com)" -H "Access-Control-Request-Method: POST" -v http://localhost:8000/api/v1/orders/assign
```

#### Kết quả: Trình duyệt sẽ tự động chặn request vì trong `HTTP` `Response` `Headers` trả về không có 

```json
Access-Control-Allow-Origin: [https://evil-competitor.com](https://evil-competitor.com).
```