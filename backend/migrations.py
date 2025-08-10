import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.models import Base
from app.config import get_settings

settings = get_settings()

async def run_migrations():
    engine = create_async_engine(settings.db_url)
    async with engine.begin() as conn:
        # Create pgvector extension if it doesn't exist
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector;'))
        
        # Drop existing tables if they exist
        await conn.execute(text('DROP TABLE IF EXISTS conversations CASCADE;'))
        await conn.execute(text('DROP TABLE IF EXISTS chunks CASCADE;'))
        await conn.execute(text('DROP TABLE IF EXISTS documents CASCADE;'))
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_migrations())
