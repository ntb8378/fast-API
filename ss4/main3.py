"""
Phần 1: Báo cáo phân tích
Input của bài toán là gì?
Danh sách sản phẩm (products) với các trường: id, name, price.
Các query parameters: keyword (string, không bắt buộc), max_price (float, không bắt buộc).
Output mong muốn là gì?
Danh sách sản phẩm thỏa mãn điều kiện tìm kiếm và lọc.
Nếu không truyền query parameter nào → trả về toàn bộ sản phẩm.
Nếu truyền keyword → lọc theo tên chứa từ khóa (không phân biệt hoa thường).
Nếu truyền max_price → lọc theo giá ≤ max_price.
Nếu truyền cả hai → sản phẩm phải thỏa mãn cả hai điều kiện.
Nếu max_price < 0 → trả về lỗi rõ ràng.
Đề xuất giải pháp xử lý:
Khai báo API GET /products.
Nhận keyword và max_price qua query parameters.
Kiểm tra max_price: nếu < 0 → trả về lỗi.
Lọc danh sách theo keyword (dùng .lower() để không phân biệt hoa thường).
Lọc tiếp theo max_price nếu có.
Trả về danh sách kết quả.
Thiết kế các bước xử lý:
Nhận request.
Kiểm tra dữ liệu đầu vào (max_price).
Áp dụng bộ lọc theo keyword.
Áp dụng bộ lọc theo max_price.
Trả về kết quả cuối cùng.
Phần 2: Triển khai code
"""

from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000},
]


@app.get("/products")
def get_products(keyword: str = Query(None), max_price: float = Query(None)):
    # Kiểm tra max_price hợp lệ
    if max_price is not None and max_price < 0:
        return {"detail": "max_price không được âm"}

    filtered = products

    # Lọc theo keyword
    if keyword:
        keyword_lower = keyword.lower()
        filtered = [p for p in filtered if keyword_lower in p["name"].lower()]

    # Lọc theo max_price
    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]
    if not filtered:
        return {"message": "Không tìm thấy đơn hàng không hợp lệ"}
    return filtered
