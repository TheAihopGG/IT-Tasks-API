import aiosqlite
from logging import *
from typing import Final
from data.settings import *

TASKS_COLUMNS = (
    "id",
    "title",
    "text"
)

async def create_tables():
    """Creates tables in DB_PATH"""
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                text TEXT
            );
        """)
        await db.commit()

        debug("Tables created")
