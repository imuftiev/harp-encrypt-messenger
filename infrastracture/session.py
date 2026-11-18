from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from settings import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.url
)

Session = async_sessionmaker(engine)


def get_session() -> AsyncSession:
    return Session()
