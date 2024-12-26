import aiosqlite
import asyncio
from logging import *
from services.database import create_tables, TASKS_COLUMNS
from data.settings import *
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()
basicConfig(level=INFO)
__doc__ = """
    GET /api/get_task/?id=<id> - returns task with <id>
    GET /api/get_tasks_ids - returns tasks ids
"""

@app.get("api/help")
async def help() -> PlainTextResponse:
    return PlainTextResponse(__doc__)


@app.get("/api/get_task")
async def get_task(id: int) -> JSONResponse:
    async with aiosqlite.connect(DB_PATH) as db:
        result = await (await db.execute(
            "SELECT * FROM tasks WHERE id=?",
            (id,)
        )).fetchone()
        if result:
            return JSONResponse(dict(zip(
                TASKS_COLUMNS,
                result
            )))

        else:
            return JSONResponse({
                "detail":{
                    "msg":f"Task not found with id: {id}"
                }
            })


@app.get("/api/get_tasks_ids")
async def get_tasks_ids() -> JSONResponse:
    async with aiosqlite.connect(DB_PATH) as db:
        result = await (await db.execute("SELECT id FROM tasks")).fetchall()
        if result:
            return JSONResponse({"ids":result[0]})

        else:
            return JSONResponse({
                "detail":{
                    "msg":"No tasks available"
                }
            })

if __name__ == "__main__":
    asyncio.run(create_tables())
