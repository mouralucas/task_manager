import contextlib
from typing import Any, AsyncIterator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine, async_sessionmaker

from backend.settings import settings
from models.task import Base


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

        @event.listens_for(self._engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    async def init_database(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self.connect() as connection:
            # Criação das tabelas
            await connection.run_sync(Base.metadata.create_all)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            """
                Closes the backend session after the context is exited.
                The commit is only applied when the context is exited.
            """
            await session.commit()
            await session.close()


sessionmanager = DatabaseSessionManager(settings.finance_database_url, {"echo": settings.echo_sql})
test_sessionmanager = DatabaseSessionManager(settings.test_database_url, {"echo": settings.echo_test_sql})


async def get_session():
    async with sessionmanager.session() as session:
        yield session