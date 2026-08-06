# Dataset inventory & students:
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

n = len(students)

for i in range(n):
    for j in range(n - i - 1):
        if students[j]["gpa"] < students[j+1]["gpa"]:
            students[j], students[j+1] = students[j+1], students[j]

for s in students:
    print(f"  -> {s['name']}: {s['gpa']} điểm")