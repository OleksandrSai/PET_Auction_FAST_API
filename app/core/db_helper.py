from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import settings


class DatabaseHelper:
    def __init__(self, url: str = settings.database_url, echo: bool = settings.db_echo):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session = async_sessionmaker(
            autoflush=False,
            bind=self.engine,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DatabaseHelper()
