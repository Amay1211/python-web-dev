from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = (True,)


class CreatePost(PostBase):
    pass


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    contact: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    contact: str
    created_at: datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    userDetails: UserResponse

    class Config:
        from_attributes = True


class PostWithVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    accessToken: str
    tokenType: str


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
