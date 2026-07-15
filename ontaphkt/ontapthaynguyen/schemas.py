from pydantic import BaseModel, Field, field_validator

class TechRentCreate(BaseModel):
    id : str
    category : str = Field(...,min_length=2,max_length=50)
    model: str
    rental_rate : float  = Field(...,gt=0)
    release_year : int =  Field(...,le=2026,ge=2018)
    status: str  = "available"

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):

        if value not in ["available", "rented", "repairing"]:
            raise ValueError(
                "sai trạng thái"
            )

        return value
