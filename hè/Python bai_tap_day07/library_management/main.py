from fastapi import FastAPI, HTTPException
from schemas import Book

app = FastAPI()

danh_sach_sach = [
    {
    "id": 1,
    "ten_sach": "Nhà Giả Kim",
    "tac_gia": "Paulo Coelho",
    "nam_xuat_ban": 1988,
    "so_luong": 5
    },
    {
    "id": 2,
    "ten_sach": "dế mèn phiêu lưu ký",
    "tac_gia": "Tô Hoài",
    "nam_xuat_ban": 1941,
    "so_luong": 5
    }

]

@app.get("/")
def home():
    return {"message":"hello"}

@app.post("/api/v1/books", response_model=Book)
def create_book(book: Book):

    new_book = {
    "id": book.id,
    "ten_sach": book.ten_sach,
    "tac_gia": book.tac_gia,
    "nam_xuat_ban": book.nam_xuat_ban,
    "so_luong": book.so_luong
}


    danh_sach_sach.append(new_book)

    return new_book

@app.get("/api/v1/books", response_model=list[Book])
def get_all_book():
    return danh_sach_sach

@app.get("/api/v1/books/{book_id}", response_model=Book)
def get_book(book_id: int):

    for book in danh_sach_sach:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

@app.put("/api/v1/books/{book_id}", response_model=Book)
def put_book(book_id: int, update_book:Book):
    for book in danh_sach_sach:
        if book["id"] == book_id:
            book["ten_sach"] = update_book.ten_sach
            book["tac_gia"] = update_book.tac_gia
            book["nam_xuat_ban"] = update_book.nam_xuat_ban
            book["so_luong"] = update_book.so_luong

            return book
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

@app.delete("/api/v1/books/{book_id}")
def delete_book(book_id:int):
    for book in danh_sach_sach:
        if book["id"] == book_id:
            danh_sach_sach.remove(book)
            return {"message": "Xóa thành công"}
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )  