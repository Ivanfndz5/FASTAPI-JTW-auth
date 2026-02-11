from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name : str
    age : int
    is_vip: bool = False


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id : int

    class Config:
        orm_mode = True


