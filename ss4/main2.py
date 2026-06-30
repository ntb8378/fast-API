"""
Phần 1: Phân tích lỗi
Endpoint hiện tại có Path Parameter không?
Có. Route được khai báo là /orders/status/{status}, trong đó {status} là Path Parameter.

Path Parameter trong bài này là gì?
Chính là status.

Khi gọi /orders/status/pending, biến status nhận giá trị gì?
Biến status nhận giá trị "pending".

Vì sao API hiện tại trả về sai dữ liệu?
Vì trong hàm get_orders_by_status, giá trị status không được sử dụng để lọc dữ liệu. Hàm chỉ trả về toàn bộ danh sách orders.

Dòng code nào đang khiến API bỏ qua giá trị status?

python
return orders
Dòng này trả về toàn bộ danh sách mà không lọc theo status.

Phần 2: Sửa code
"""

from fastapi import FastAPI

app = FastAPI()

orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"},
]


@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    valid_statuses = ["pending", "paid", "cancelled"]
    if status not in valid_statuses:
        return {"message": "Trạng thái đơn hàng không hợp lệ"}

    filtered_orders = [order for order in orders if order["status"] == status]
    return filtered_orders
