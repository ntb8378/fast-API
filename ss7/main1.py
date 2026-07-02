from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Dữ liệu nội bộ trong bộ nhớ tạm - Chứa các trường nhạy cảm
orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,      # Nhạy cảm - Cấm lộ!
        "supplier_id": "SUP_DELL_01" # Nhạy cảm - Cấm lộ!
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,       # Nhạy cảm - Cấm lộ!
        "supplier_id": "SUP_LOGI_02"  # Nhạy cảm - Cấm lộ!
    }
]

class OrderInternal(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    profit_margin: float
    supplier_id: str

@app.get("/orders/{order_id}")
def get_order_detail(order_id: int):
    for order in orders_db:
        if order["id"] == order_id:
            return order 
    return {"message": "Order not found"}



# Câu 5. Chỉ ra lỗi bằng test case

# | STT | Dữ liệu gửi lên | Kết quả hiện tại (Mã HTTP + Body) | Kết quả đúng mong muốn | Lỗi phát hiện |
# |-----|------------------|-----------------------------------|------------------------|---------------|
# | 1 | order_id = 999 | HTTP 200 OK<br>Body: {"message": "Order not found"} | HTTP 404 Not Found<br>Body: {"detail": "Order not found"} | Sai mã trạng thái HTTP, API trả về 200 thay vì 404 khi không tìm thấy đơn hàng. |
# | 2 | order_id = 1 | HTTP 200 OK<br>Body: {"id":1,"customer_name":"Nguyen Van A","total_amount":1500000.0,"profit_margin":0.25,"supplier_id":"SUP_DELL_01"} | HTTP 200 OK<br>Body chỉ gồm: {"id":1,"customer_name":"Nguyen Van A","total_amount":1500000.0} | Lộ thông tin nhạy cảm do trả về hai trường `profit_margin` và `supplier_id`. |