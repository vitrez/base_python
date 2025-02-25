import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload

from models import Base, engine, User, Post, async_session_factory
from jsonplaceholder_requests import fetch_json


USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def create_users(session: AsyncSession, users_data: dict) -> list[User]:
    users = [User(**user) for user in users_data]
    session.add_all(users)
    await session.commit()
    return users


async def create_posts(session: AsyncSession, posts_data: dict) -> list[Post]:
    posts = [Post(**post) for post in posts_data]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(
    session: AsyncSession,
) -> list[User]:
    stmt = (
        # получить всех юзеров
        select(User)
        # join for ORM
        .options(
            # to many -> selectinload
            selectinload(User.posts),
        )
        # обязательно сортируем
        .order_by(User.id)
    )

    users = (await session.scalars(stmt)).all()
    for user in users:
        print("user:", user)
        print("user's posts:")
        for post in user.posts:
            print("+ post:", post)
    return list(users)


async def get_posts_with_users(
    session: AsyncSession,
) -> list[Post]:
    stmt = (
        # берем все посты
        select(Post)
        # присоединяем для ORM
        .options(
            # to one -> joinedload
            joinedload(Post.user)
        )
        # обязательно сортируем
        .order_by(Post.id)
    )

    result = await session.scalars(stmt)
    posts = result.all()
    for post in posts:
        print(post, "author: ", post.user.name)
    return list(posts)


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    users_data, posts_data = await asyncio.gather(
        fetch_json(USERS_DATA_URL),
        fetch_json(POSTS_DATA_URL),
    )

    async with async_session_factory() as session:
        await create_users(session, users_data)

    async with async_session_factory() as session:
        await create_posts(session, posts_data)

    async with async_session_factory() as session:
        await get_users_with_posts(session)
        await get_posts_with_users(session)


if __name__ == "__main__":
    asyncio.run(async_main())
