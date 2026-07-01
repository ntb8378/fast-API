from fastapi import FastAPI,HTTPException
from pydantic import  BaseModel,Field


class createCourse(BaseModel):
    code : str | None
    name: str | None
    duration: int | None  = Field(...,gt= 0)
    fee: float | None = Field(...,ge= 0)
class updateCourse(BaseModel):
    code : str | None
    name: str 
    duration: int  = Field(...,gt= 0)
    fee: float | None = Field(...,ge= 0)
 

app = FastAPI()

courses = [
{"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
{"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
{"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

@app.get("/")
def root():
    return {"mess": "Hello"}

@app.get("/courses")
def get_courses():
    if courses is None: 
        raise HTTPException(status_code=404,detail="Không tìm có khóa học nào")
    else:
        return courses
@app.get("/courses/{course_id}")
def get_course(course_id : int):
    for course in courses:
        if course_id == course["id"]:
            return course
    else:
        raise HTTPException(status_code=404,detail="Không tìm có khóa học") 

@app.post("/courses")
def create_course(course: createCourse):
    new_id = max((s["id"] for s in courses), default = 0) + 1
    new_course = {
        "id" : new_id,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }
    courses.append(new_course)
    return new_course

@app.put("/courses/{course_id}")
def update_course(course_id : int , update_course : updateCourse):
    for course in courses:
        if course_id == course.get("id"):
            new_course = {
                "code": update_course.code | course["code"],
                "name": update_course.name | course["name"] ,
                "duration": update_course.duration | course["duration"],
                "fee" : update_course.fee | course["fee"]} 
            course = new_course
    else:
        raise HTTPException(status_code=404,detail="không tìm thấy khóa học")

@app.delete("/courses/{course_id}")
def delete_course(course_id):
    for course in courses:
        if course_id == course.get("id"):
            courses.remove(course)
    else:
        raise HTTPException(status_code=404,detail="không tìm thấy khóa học")
    
     



    


