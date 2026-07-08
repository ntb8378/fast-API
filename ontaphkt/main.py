from fastapi import FastAPI

app = FastAPI(title="Hệ thống phân tích đơn hàng")

mock_orders = [
    {"id": 1, "customer_name": "Nguyen Van A", "total_amount": 500000, "status": "delivered"},
    {"id": 2, "customer_name": "Tran Thi B", "total_amount": 200000, "status": "pending"},
    {"id": 3, "customer_name": "Nguyen Van A", "total_amount": 350000, "status": "delivered"},
    {"id": 4, "customer_name": "Le Van C", "total_amount": 350000, "status": "delivered"},
    {"id": 5, "customer_name": "Tran Thi B", "total_amount": 500000, "status": "delivered"},
    {"id": 6, "customer_name": "Pham Van D", "total_amount": 150000, "status": "cancelled"},
]


@app.get("/orders/revenue-report")
def get_orders_revenue_report():
    total_orders = 0
    total_revenue = 0
    average_order_value = 0
    successful_revenue = 0

    if not mock_orders:
        return {"message": "Danh sách rỗng!"}

    for order in mock_orders:
        total_orders += 1
        total_revenue += order["total_amount"]
        if order["status"] == "delivered":
            successful_revenue += order["total_amount"]

    if total_orders > 0:
        average_order_value = total_revenue / total_orders

    return {
        "total_revenue": total_revenue,
        "successful_revenue": successful_revenue,
        "average_order_value": average_order_value,
    }

@app.get("/orders/status-breakdown")
def get_orders_status_breakdown():
    pending =0
    delivered =0
    cancelled =0

    for order in mock_orders:
        if order["status"] == "pending":
            pending += 1
        elif order["status"] == "delivered":
            delivered += 1
        elif order["status"] == "cancelled":
            cancelled += 1

    return{
        "breakdown": {
        "pending": pending,
        "delivered": delivered,
        "cancelled": cancelled
    }
}

@app.get("/orders/top-customers")
def get_orders_top_customers():

    # Dictionary dùng để lưu tổng tiền của từng khách hàng.
    # Sau khi chạy xong sẽ có dạng:
    # {
    #     "Nguyen Van A": 850000,
    #     "Tran Thi B": 500000,
    #     "Le Van C": 350000
    # }
    customer_total = {}

    # Duyệt từng đơn hàng trong danh sách
    for order in mock_orders:

        # Nếu đơn hàng KHÔNG phải đã giao
        # thì bỏ qua và chuyển sang đơn tiếp theo
        if order["status"] != "delivered":
            continue

        # Lấy tên khách hàng
        name = order["customer_name"]

        # Nếu khách hàng chưa có trong dictionary
        # thì tạo mới với tổng tiền ban đầu = 0
        if name not in customer_total:
            customer_total[name] = 0

        # Cộng tiền của đơn hàng hiện tại
        # Ví dụ:
        # Nguyễn Văn A đang có 500000
        # Đơn hiện tại là 350000
        # => 500000 + 350000 = 850000
        customer_total[name] += order["total_amount"]

    # customer_total.items() sẽ biến dictionary thành
    # một danh sách các cặp (tên khách, tổng tiền)
    #
    # Ví dụ:
    # {
    #   "Nguyen Van A":850000,
    #   "Tran Thi B":500000
    # }
    #
    # sẽ thành
    #
    # [
    #   ("Nguyen Van A",850000),
    #   ("Tran Thi B",500000)
    # ]

    # sorted() dùng để sắp xếp danh sách
    #
    # key=lambda item: item[1]
    # nghĩa là:
    # Khi sắp xếp hãy nhìn vào phần tử thứ 2
    #
    # ("Nguyen Van A",850000)
    #      item[0]        item[1]
    #
    # item[1] chính là tổng tiền
    #
    # reverse=True nghĩa là sắp xếp từ lớn xuống nhỏ
    sorted_customer = sorted(
        customer_total.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # Lấy 3 phần tử đầu tiên
    top3 = sorted_customer[:3]

    # Trả kết quả
    return top3