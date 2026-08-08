from fastapi import FastAPI
from database import Base, engine
from router import router

app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(router)

@app.get("/")
def test():
    return{
        "message" : "kết nối thành công"
    }
