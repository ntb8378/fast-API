# | STT | Dữ liệu gửi lên                              | Kết quả hiện tại                    | Kết quả đúng mong muốn                                 | Lỗi phát hiện                    |
# | --- | -------------------------------------------- | ----------------------------------- | ------------------------------------------------------ | -------------------------------- |
# | 1   | `code = "SP001"` (đã tồn tại trong hệ thống) | API vẫn tạo sản phẩm mới thành công | API phải báo lỗi mã sản phẩm đã tồn tại, không tạo mới | Không kiểm tra trùng mã sản phẩm |
# | 2   | `code = "SP002"` (đã tồn tại trong hệ thống) | API vẫn tạo sản phẩm mới thành công | API phải báo lỗi mã sản phẩm đã tồn tại, không tạo mới | Không kiểm tra trùng mã sản phẩm |


# phần 2:
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):

    # Kiểm tra trùng mã sản phẩm
    for p in products:
        if p["code"] == product.code:
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }