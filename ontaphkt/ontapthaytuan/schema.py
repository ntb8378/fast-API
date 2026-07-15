from pydantic import BaseModel


class TeamsCreate(BaseModel):

    country_name : str
    coach_name : str
    group_name : str