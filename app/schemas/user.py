from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_admin: bool

    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
