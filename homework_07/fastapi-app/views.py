from typing import Annotated
from fastapi import (
    APIRouter,
    status,
    Depends,
)
from schemas import UserRead, UserCreate, PostCreate, PostRead
from crud import User, Post
from dependencies import (
    posts_crud_dependency,
    users_crud_dependency,
    add_user_crud_dependency,
    add_post_crud_dependency,
)


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

posts_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@users_router.get(
    "/",
    response_model=list[UserRead],
)
def get_users_list(
    users: Annotated[
        list[User],
        Depends(users_crud_dependency),
    ],
):
    return users


@users_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreate,
)
def create_user(
    user_added: Annotated[
        User,
        Depends(add_user_crud_dependency),
    ],
):
    return user_added


@posts_router.get(
    "/",
    response_model=list[PostRead],
)
def get_posts_list(
    posts: Annotated[
        list[Post],
        Depends(posts_crud_dependency),
    ],
):
    return posts


@posts_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostCreate,
)
def create_post(
    post_added: Annotated[
        Post,
        Depends(add_post_crud_dependency),
    ],
):
    return post_added
