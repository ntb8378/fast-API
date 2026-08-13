from pydantic import BaseModel, ConfigDict


class ClassroomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    class_code: str
    class_name: str
    max_students: int
    status: str
