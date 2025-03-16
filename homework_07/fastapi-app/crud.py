import asyncio
import aiohttp
from sqlalchemy import select, text
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload
from typing import Any

from schemas import UserCreate, PostCreate
from models import User, Post, async_session_factory


USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(url: str) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def create_users(users_data: dict, session: AsyncSession) -> list[User]:
    users = [User(**user) for user in users_data]
    session.add_all(users)
    await session.commit()
    return users


async def setval_users(session: AsyncSession):
    statement = func.max(User.id)
    maxid = await session.scalars(statement)
    newid = maxid.all()
    statement = text(
        """select setval('user_id_seq',""" + str(newid[0]) + """) FROM user"""
    )
    await session.scalars(statement)


async def add_user(user_in: UserCreate, session: AsyncSession) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def create_posts(posts_data: dict, session: AsyncSession) -> list[Post]:
    posts = [Post(**post) for post in posts_data]
    session.add_all(posts)
    await session.commit()
    return posts


async def add_post(post_in: PostCreate, session: AsyncSession) -> Post:
    post = Post(**post_in.model_dump())
    session.add(post)
    await session.commit()
    return post


async def setval_posts(session: AsyncSession):
    statement = func.max(Post.id)
    maxid = await session.scalars(statement)
    newid = maxid.all()
    statement = text(
        """select setval('post_id_seq',""" + str(newid[0]) + """) FROM post"""
    )
    await session.scalars(statement)


async def check_db_empty(session: AsyncSession) -> bool:
    statement = select(User).limit(1)
    result = await session.execute(statement)
    if result.scalar() is None:
        return True
    else:
        return False


async def filling_db() -> None:
    # Закомментировали код ниже, поскольку создание пустых таблиц будет через Alembic
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        db_empty = await check_db_empty(session)

    if db_empty:

        users_data, posts_data = await asyncio.gather(
            fetch_json(USERS_DATA_URL),
            fetch_json(POSTS_DATA_URL),
        )

        async with async_session_factory() as session:
            await create_users(users_data, session)
            await setval_users(session)

        async with async_session_factory() as session:
            await create_posts(posts_data, session)
            await setval_posts(session)


async def get_users_with_posts(
    session: AsyncSession,
) -> list[User]:
    statement = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(statement)
    return list(users)


async def get_posts_with_users(
    session: AsyncSession,
) -> list[Post]:
    statement = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(statement)
    return list(posts)


if __name__ == "__main__":
    asyncio.run(filling_db())
