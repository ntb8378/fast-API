from fastapi import FastAPI, Depends, HTTPException
from database import *
from sqlalchemy.orm import Session
from sqlalchemy import text
app = FastAPI()

@app.get("/test")
def test(db: Session = Depends(get_db)):
    try:
        db. execute(text('SELECT 1'))

        return {
            "status_code": 200,
            "message": "Ket noi thanh cong đen DB"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Ket noi thất bại")