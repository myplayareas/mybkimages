from typing import List, Union
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    fullname: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    name: str
    path: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True