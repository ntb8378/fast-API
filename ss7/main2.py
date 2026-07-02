from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

class StatusUpdate(BaseModel):
    status: str

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return next((o for o in orders_db if o["id"] == order_id), None)

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    
    if not order:
        print("Order not found!") 
        
    if data.status not in ["PENDING", "SHIPPING", "DELIVERED"]:
        return {"error": "Trạng thái không hợp lệ"} 
        
    if order:
        order["status"] = data.status

    return {"statusCode": 200, "message": "Cập nhật thành công", "data": order}

    # Câu 5. Chỉ ra lỗi bằng test case

# | STT | Dữ liệu/Endpoint gửi lên | Kết quả hiện tại (Mã HTTP + Body) | Kết quả đúng mong muốn | Lỗi phát hiện |
# |-----|---------------------------|-----------------------------------|------------------------|---------------|
# | 1 | PUT /orders/999/status với status="SHIPPING" | HTTP 200 OK<br>Body: {"statusCode":200,"message":"Cập nhật thành công","data":null} | HTTP 404 Not Found<br>Body: {"detail":"Order not found"} | Không dùng `raise HTTPException(404)` khi không tìm thấy đơn hàng, chỉ `print()` nên API vẫn trả về 200 OK. |
# | 2 | PUT /orders/1/status với status="TRONG_SANG" | HTTP 200 OK<br>Body: {"error":"Trạng thái không hợp lệ"} | HTTP 400 Bad Request<br>Body: {"detail":"Trạng thái không hợp lệ"} | Xử lý lỗi sai, dùng `return` thay vì `raise HTTPException(400)`, nên API vẫn trả về 200 OK khi trạng thái không hợp lệ. |