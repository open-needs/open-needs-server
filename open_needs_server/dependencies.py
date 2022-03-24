from sqlalchemy.ext.asyncio import AsyncSession

from open_needs_server.database import async_session_maker

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


