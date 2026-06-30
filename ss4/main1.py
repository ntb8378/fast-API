"""
Phần 1: Phân tích lỗi
Vì sao GET /products/1 trả về 404?  
Vì route hiện tại được khai báo là /products/product_id (chuỗi cố định), chứ không phải path parameter. Do đó, khi gọi /products/1, FastAPI không tìm thấy route phù hợp.

Dòng code khai báo sai Path Parameter:

python
@app.get("/products/product_id")
Đây là lỗi vì thiếu dấu {} để khai báo biến động.

Vì sao /products/product_id không phải Path Parameter?  
Vì FastAPI hiểu product_id ở đây là một đoạn đường dẫn tĩnh, giống như /products/abc. Muốn biến động thì phải dùng {product_id}.

Endpoint đúng cần sửa thành gì?

python
@app.get("/products/{product_id}")
Phần 2: Sửa code
"""

from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000},
]


@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    """Trả về chi tiết sản phẩm tìm được"""
    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Không tìm thấy sản phẩm"}
