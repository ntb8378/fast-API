# Dataset orders:
orders = [
    {"id": "DH01", "name": "iPhone 15 Pro Max", "price": 32000000},
    {"id": "DH02", "name": "Tai nghe AirPods Pro", "price": 5500000},
    {"id": "DH03", "name": "MacBook Pro M3 Max", "price": 65000000},
    {"id": "DH04", "name": "Chuot khong day", "price": 450000},
    {"id": "DH05", "name": "Samsung Galaxy S24", "price": 22000000}
]

total_revenue = 0
vip_order_count = 0

max_order = orders[0]
min_order = orders[0]

is_suspicious = False

for order in orders:
    total_revenue += order["price"]
    if order["price"] >= 15000000:
        vip_order_count += 1
    if order["price"] >= 50000000:
        is_suspicious = True
        suspicious = order

    if order["price"] > max_order["price"]:
        max_order = order
    if order["price"] < min_order["price"]:
        min_order = order


print(f"Tong doanh thu: {total_revenue}")
print(f"So don hang VIP (>= 15tr): {vip_order_count}")
print(f"Don hang gia tri CAO NHAT: {max_order["id"]} - {max_order["name"]} ({max_order["price"]} VND)")
print(f"Don hang gia tri THAP NHAT: {min_order["id"]} - {min_order["name"]} ({min_order["price"]} VND)")
print(f"CANH BAO RUI RO: Phat hien don {suspicious["id"]} co gia tri {suspicious["price"]} VND > 50tr!")
print("KET LUAN CAM CO: Co is_suspicious = True")