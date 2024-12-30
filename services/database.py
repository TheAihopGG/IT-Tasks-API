import aiosqlite
from logging import *
from typing import Final
from data.settings import *

TASKS_COLUMNS = (
    'id',
    'image_url',
    'title',
    'topic',
    'task',
    'answer',
    'tags'
)

async def create_tables():
    '''Creates tables in DB_PATH'''
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                image_url TEXT,
                title TEXT,
                topic TEXT,
                task TEXT,
                answer TEXT,
                tags JSON DEFAULT []
            );
        ''')
        await db.commit()

        debug('Tables created')
