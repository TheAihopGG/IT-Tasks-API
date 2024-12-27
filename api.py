import aiosqlite
import asyncio
from services.responses import *
from logging import *
from services.database import create_tables, TASKS_COLUMNS
from data.settings import *
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()
basicConfig(level=INFO)
__doc__ = '''
    GET /api/task/ - returns task with <id>
    GET /api/get_tasks_ids - returns tasks ids
'''

@app.get('api/help')
async def help() -> PlainTextResponse:
    # return
    return PlainTextResponse(__doc__)


@app.get('/api/task')
async def get_task(request: Request) -> JSONResponse:
    # get values from headers
    id: int = request.headers.get('id', None)
    # validate
    if id < 0:
        return ErrorResponse(f'Id must be bigger than 0')
    # return
    async with aiosqlite.connect(DB_PATH) as db:
        if task := await (await db.execute(
            'SELECT * FROM tasks WHERE id=?',
            (id,)
        )).fetchone():
            return JSONResponse(dict(zip(
                TASKS_COLUMNS,
                task
            )))

        else:
            return ErrorResponse(f'Task not found')


@app.get('/api/tasks/ids')
async def get_tasks_ids() -> JSONResponse:
    # just returns all tasks ids
    async with aiosqlite.connect(DB_PATH) as db:
        if tasks_ids := await (await db.execute('SELECT id FROM tasks')).fetchall():
            return JSONResponse({'ids':tasks_ids[0]})

        else:
            return ErrorResponse('No tasks available')


@app.get('/api/task/by_tags')
async def get_tasks_by_tags(request: Request) -> JSONResponse:
    # get values from headers
    tags: list[str] = request.headers.get('tags', None)
    # validate
    if not tags:
        return ErrorResponse(f'Tags are required')
    
    elif not isinstance(tags, list):
        return ErrorResponse(f'Tags must be array')
    
    elif len(tags) in range(1, MAX_REQUEST_TAGS_COUNT):
        return ErrorResponse(f'Limited max tags count. The limit is: {MAX_REQUEST_TAGS_COUNT}')
    # return
    async with aiosqlite.connect(DB_PATH) as db:
        if tasks := [dict(zip(TASKS_COLUMNS, task)) for task in await (await db.execute('SELECT * FROM tasks'))]:
            if tasks_with_tag := [task if all(tag in task['tags'] for tag in tags) else None for task in tasks]:
                return JSONResponse({'tasks':tasks_with_tag})
            else:
                return ErrorResponse(f'Tasks has not found with these tags: {tags}')

if __name__ == '__main__':
    asyncio.run(create_tables())
