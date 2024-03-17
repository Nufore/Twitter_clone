import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.config import settings
from core.models import Base, db_helper


from users.views import router as users_router

# from database import Base, engine, session
# from models import User, followers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # await db_helper.session_factory.close()
    # await db_helper.engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router=users_router, prefix=settings.api_prefix)

templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/create_users")
# async def create_users():
#     async with session.begin():
#         session.add_all(
#             [
#                 User(name='test user', api_key='test'),
#                 User(name='qwe user', api_key='qwe'),
#                 User(name='zxc user', api_key='zxc'),
#             ]
#         )
#         await session.commit()
#     return {"message": "users created!"}
#
#
# @app.post("/api/users/{user_id}/follow")
# async def follow_user(user_id: int, request: Request):
#     api_key = request.headers.get("Api-Key")
#     async with session.begin():
#         res = await session.execute(select(User).where(User.api_key == api_key))
#         user_me = res.scalars().one_or_none()
#
#         res = await session.execute(select(User).where(User.id == user_id))
#         user_to_follow = res.scalars().one_or_none()
#
#         stmt = select(followers).filter(
#             followers.c.follower_id == user_me.id, followers.c.followed_id == user_to_follow.id
#         )
#         kk = await session.execute(stmt)
#         is_followed = kk.scalars().all()
#
#         if not is_followed:
#             user_me.followed.append(user_to_follow)
#
#         # user_me.follow(user_to_follow)
#         await session.commit()
#     return {"result": True}


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="localhost",
        port=8000,
        reload=True
    )
