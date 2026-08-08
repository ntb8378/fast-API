from sqlalchemy.orm import Session
from schemas.schemas import BookUpdate
from models.models import BookModel


def update_book(db:Session,book_id:int, book_in:BookUpdate):
    find_id=db.query(BookModel).filter(BookModel.id == book_id).first()
    if find_id:
        book_data = book_in.model_dump(exclude_unset=True)

        for field, value in book_data.items():
            setattr(find_id, field, value)

        db.commit()
        db.refresh(find_id)
        return find_id

def delete_book(db: Session, book_id: int) -> bool:
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        return False 
    db.delete(db_book)  
    db.commit()
    return True