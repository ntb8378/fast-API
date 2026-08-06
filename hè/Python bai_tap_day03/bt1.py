inventory = [
    {"id": "SP1", "ten": "Tai nghe Sony", "gia": 1200000, "danh_muc": "Phụ kiện"},
    {"id": "SP2", "ten": "Chuột không dây", "gia": 450000, "danh_muc": "Phụ kiện"},
    {"id": "SP3", "ten": "Bàn phím Cơ", "gia": 950000, "danh_muc": "Phụ kiện"},
    {"id": "SP4", "ten": "Màn hình Dell 27 inch", "gia": 4500000, "danh_muc": "Thiết bị"},
    {"id": "SP5", "ten": "Sạc dự phòng 20000mAh", "gia": 350000, "danh_muc": "Phụ kiện"}
]

students = [
    {"name": "An", "gpa": 7.2},
    {"name": "Bình", "gpa": 9.5},
    {"name": "Cường", "gpa": 6.8},
    {"name": "Dũng", "gpa": 8.4}
]

def linear_search_filter(cart, target_category, max_price):
    result = []
    for pro in cart:
        if pro["gia"] <= max_price and pro["danh_muc"] == target_category:
            result.append(pro)
            print(f'-> [{pro["id"]}] {pro["ten"]} | Giá: {pro["gia"]} VNĐ')
    return result
print(f"KẾT QUẢ LỌC SẢN PHẨM (LINEAR SEARCH MULTI-CRITERIA)")
print(f"Danh mục tìm kiếm: Phụ kiện | Giá tối đa: 1,000,000 VNĐ")

linear_search_filter(inventory, "Phụ kiện", 1000000)