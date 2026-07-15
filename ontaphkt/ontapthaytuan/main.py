from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from models import TeamsModel
from sqlalchemy.orm import Session
import teams_service
from schema import TeamsCreate

app = FastAPI(
    title="QUẢN LÝ ĐỘI TUYỂN WORLD CUP"
)

Base.metadata.create_all(bind= engine)

@app.get("/")
def test():
    return{
        "message" : "Kết nối thành công!"
    }


@app.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    return teams_service.get_teams(db)

@app.get("/teams/search")
def search_team( name:str ,db: Session = Depends(get_db)):
    return teams_service.search_team(db,name)

@app.get("/teams/sort")
def sort(sort_name:str ="desc",db:Session = Depends(get_db)):
    return teams_service.sort_team(db,sort_name)

@app.get("/teams/{team_id}")
def get_team_by_id(team_id : int ,db: Session = Depends(get_db)):
    return teams_service.get_team_by_id(db, team_id)


@app.post("/teams")
def post_team(input_team: TeamsCreate ,db: Session = Depends(get_db)):
    return teams_service.post_team(db, input_team)

@app.put("/teams/{team_id}")
def put_team(team_id:int ,update_team: TeamsCreate ,db: Session = Depends(get_db)):
    return teams_service.put_team(db,team_id,update_team)

@app.delete("/teams/{team_id}")
def delete_team(team_id:int ,db: Session = Depends(get_db)):
    return teams_service.delete_team(db, team_id)

