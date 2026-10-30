from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    student_id: str

class UserRead(BaseModel):
    id: int = Field(validation_alias="userid")   
    name: str
    email: str
    age: int
    student_id: str

    model_config = {"from_attributes": True}