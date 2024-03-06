import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database import Base, engine, session
from models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")


@app.get("/create_users")
async def create_users():
    async with session.begin():
        session.add_all(
            [
                User(name='test user', api_key='test'),
                User(name='qwe user', api_key='qwe'),
                User(name='zxc user', api_key='zxc'),
            ]
        )
        await session.commit()


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/api/users/{nickname}")
# async def get_users(request: Request, nickname: str):
#     return {"message": f"hello, {nickname}"}


# @app.get("/login")
# async def get_users(request: Request):
#     return {"query": 123, "nickname": "test"}


@app.get("/api/tweets")
async def get_tweets():
    data = {
        "result": True,
        "tweets": [
            {
                "id": 1,
                "content": "test tweet",
                "attachments": [],
                "author": {
                    "id": 1,
                    "name": "test author"
                },
                "likes": [
                    {
                        "user_id": 2,
                        "name": "test_user"
                    }
                ],
            },
        ]
    }
    return data


@app.get("/api/users/me")
async def get_users_me(request: Request):
    api_key = request.headers.get("Api-Key")
    async with session.begin():
        res = await session.execute(select(User).where(User.api_key == api_key))
        user_from_db = res.scalar_one_or_none()
    data = {
        "result": True,
        "user": {
            "id": user_from_db.id,
            "name": user_from_db.name,
            "followers": [
                {
                    "id": 2,
                    "name": "test user 2"
                },
                {
                    "id": 3,
                    "name": "test user 3"
                },
            ],
            "following": [
                {
                    "id": 3,
                    "name": "test user 3"
                },
            ]
        }
    }
    return data


@app.post("/api/users/{user_id}/follow")
async def follow_user(user_id: int, request: Request):
    api_key = request.headers.get("Api-Key")
    async with session.begin():
        res = await session.execute(select(User).where(User.api_key == api_key))
        user_me = res.scalar_one_or_none()

        res = await session.execute(select(User).where(User.id == user_id))
        user_to_follow = res.scalar_one_or_none()

        user_me.follow(user_to_follow)
    return {"result": True}


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="localhost",
        port=8000
    )
