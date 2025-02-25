from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr


db_url = "postgresql+asyncpg://app:apppassword@localhost:5432/blog"
# db_url = os.environ.get("SQLALCHEMY_PG_CONN_URI")
db_echo = False

engine = create_async_engine(
    db_url,
    echo=db_echo,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        unique=True,
    )
    address: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )
    phone: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )
    website: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )
    company: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id},"
            f" name={self.name!r},"
            f" username={self.username!r},"
            f" email={self.email!r}"
            f")"
        )


class Post(Base):
    userId: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        nullable=False,
    )
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        back_populates="posts",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id},"
            f" title={self.title!r},"
            f" user_id={self.userId!r}"
            f")"
        )
