from pydantic import BaseModel

class Book(BaseModel):
    id: int
    ten_sach: str
    tac_gia :str
    nam_xuat_ban :int
    so_luong :int
