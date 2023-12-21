from contextvars import ContextVar, Token

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, declarative_base

from backend.core.config import config

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engine = create_async_engine(config.MARIADB_URL, pool_recycle=3600, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
