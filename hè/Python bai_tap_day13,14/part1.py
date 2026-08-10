
raw_products = [
    {"product_code": " p101 ", "name": "Chuot Logitech", "price": 500000, "stock": 50, "status": "available"},
    {"product_code": "P102", "name": "Ban phim Co", "price": 1200000, "stock": 15, "status": "available"},
    {"product_code": "P202", "name": "Man hinh LG 27", "price": 6000000, "stock": 0, "status": "out_of_stock"},
    {"product_code": "P301", "name": "Laptop Dell XPS", "price": 25000000, "stock": 10, "status": "available"},
    {"product_code": "P302", "name": "Tai nghe Sony", "price": 3500000, "stock": 8, "status": "available"}
]
raw_orders = [
    {"order_code": "ORD081", "customer": "Nguyen Van A", "amount": 15000000, "status": "COMPLETED"},
    {"order_code": "ORD002", "customer": "Tran Thi B", "amount": 2500000, "status": "COMPLETED"},
    {"order_code": "ORD003", "customer": "Le Van C", "amount": 8000000, "status": "PENDING"},
    {"order_code": "ORD004", "customer": "Pham Van D", "amount": 45000000, "status": "COMPLETED"}
]

def clean_and_validate_products(raw_products):
    result = []
    for pro in raw_products:
        clean_code = pro["product_code"].strip().upper()
        if clean_code.startswith("P") and clean_code[1:].isdigit() and len(clean_code[1:]) == 3:
            pro["product_code"] = clean_code

            result.append(pro)

    return result

print(clean_and_validate_products(raw_products))




def binary_search_product(products, target_code):
    left = 0
    right = len(raw_products) -1

    while left <= right:
        mid = (left + right) // 2
        if products[mid]["product_code"][1:] < target_code[1:]:
            left = mid +1
        elif products[mid]["product_code"][1:] > target_code[1:]:
            right = mid - 1
        else:
            return mid 

    return{
        "message": "không tìm thấy"
    }

print(binary_search_product(raw_products, "P301"))


def analyze_order_stats(orders):
    finali_total = 0
    max_amount = 0
    order_code = ""

    for order in orders:
        if order["status"] == "COMPLETED":
            finali_total += order["amount"]

        if order["amount"] > max_amount:
            max_amount = order["amount"]
            order_code = order["order_code"]

    return {"total_revenue": finali_total, "max_order": order_code}

print(analyze_order_stats(raw_orders))
