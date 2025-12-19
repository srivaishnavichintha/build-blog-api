from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    email: EmailStr

class AuthorOut(AuthorCreate):
    id: int

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author: AuthorOut

    class Config:
        from_attributes = True
