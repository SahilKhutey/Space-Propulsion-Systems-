import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


db_url = settings.DATABASE_URL
fallback_url = "sqlite+aiosqlite:///./propsim.db"

try:
    if "postgresql" in db_url:
        engine = create_async_engine(
            db_url,
            echo=settings.DEBUG,
            pool_size=10,
            max_overflow=20
        )
    else:
        engine = create_async_engine(db_url, echo=settings.DEBUG)
except Exception as e:
    logger.warning(f"Failed to create engine for {db_url}: {e}. Falling back to SQLite.")
    engine = create_async_engine(fallback_url, echo=settings.DEBUG)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    global engine, AsyncSessionLocal
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        if "postgresql" in str(engine.url):
            logger.warning(f"Database initialization failed with PostgreSQL: {e}. Re-trying with SQLite fallback...")
            engine = create_async_engine(fallback_url, echo=settings.DEBUG)
            AsyncSessionLocal = async_sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully with SQLite fallback.")
        else:
            logger.error(f"Database initialization failed: {e}")
            raise e
