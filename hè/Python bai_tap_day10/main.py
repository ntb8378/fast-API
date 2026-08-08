from fastapi import FastAPI
from database import Base, engine
from routers import book_router

app = FastAPI()

app.include_router(book_router.router)

Base.metadata.create_all(bind= engine)


@app.get("/")
def test():
    return {
        "message": "kết nối thành công!"
    }
