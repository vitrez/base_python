from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

UserIdType = int


class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: UserIdType = Field()


class PostBase(BaseModel):
    title: str
    body: str
    userId: int


class PostRead(PostBase):
    id: UserIdType = Field()


class PostCreate(PostBase):
    pass
