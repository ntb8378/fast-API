from sqlalchemy.orm import Session
from models import TeamsModel
from fastapi import HTTPException, status
from schema import TeamsCreate

def search_team(db:Session, name:str):
    return db.query(TeamsModel).filter(TeamsModel.country_name.like(f"%{name}%")).all()
    
def sort_team(db: Session , sort_name: str = "desc"):
    query = db.query(TeamsModel)
    if sort_name == "asc":
        return query.order_by(TeamsModel.country_name.asc()).all()
    
    return query.order_by(TeamsModel.country_name.desc()).all()

def get_teams(db:Session):
    return db.query(TeamsModel).all()

def get_team_by_id(db:Session , team_id: int):
    find_id = db.query(TeamsModel).filter(TeamsModel.id == team_id).first()
    if not find_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="không tìm thấy")
    return find_id

def post_team(db:Session , input_team: TeamsCreate):
    new_team = TeamsModel(
        country_name = input_team.country_name,
        coach_name = input_team.coach_name,
        group_name = input_team.group_name
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team

def put_team(db:Session , team_id: int, update_team: TeamsCreate):
    find_id = get_team_by_id(db,team_id)
    find_id.coach_name = update_team.coach_name
    find_id.country_name = update_team.country_name
    find_id.group_name = update_team.group_name

    db.commit()
    db.refresh(find_id)
    return find_id

def delete_team(db:Session , team_id :int):
    find_id = get_team_by_id(db,team_id)
    db.delete(find_id)
    db.commit()

    return f"đã xóa {find_id}"