from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import async_session_factory, Post, User
from crud import get_users_with_posts, get_posts_with_users, add_user, add_post
from schemas import UserCreate, PostCreate


async def async_session_dependency() -> AsyncGenerator[AsyncSession, None, None]:
    async with async_session_factory() as session:
        yield session


async def users_crud_dependency(
    session: AsyncSession = Depends(async_session_dependency),
) -> list[User]:
    return await get_users_with_posts(session=session)


async def posts_crud_dependency(
    session: AsyncSession = Depends(async_session_dependency),
) -> list[Post]:
    return await get_posts_with_users(session=session)


async def add_user_crud_dependency(
    user_in: UserCreate,
    session: AsyncSession = Depends(async_session_dependency),
) -> User:
    return await add_user(user_in=user_in, session=session)


async def add_post_crud_dependency(
    post_in: PostCreate,
    session: AsyncSession = Depends(async_session_dependency),
) -> Post:
    return await add_post(post_in=post_in, session=session)
