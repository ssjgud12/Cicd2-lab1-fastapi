from typing import Annotated 
from pydantic import BaseModel, EmailStr, Field, StringConstraints 
 
NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)] 
StudentIdStr = Annotated[str, StringConstraints(pattern=r"^S\d{7}$")] 
 
# This arrives in, no id is known
class UserCreate(BaseModel): 
    name: NameStr 
    email: EmailStr 
    age: int = Field(gt=18, lt=120) 
    student_id: StudentIdStr
    
# This is what we return, the id is known as the db created it
class UserRead(BaseModel): 
    userid: int          # <--- CHANGED from user_id to userid
    name: NameStr 
    email: EmailStr 
    age: int = Field(gt=18, lt=120)
    student_id: StudentIdStr

  