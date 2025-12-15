"""
Hamster game Backend Entrance
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """using lifespan"""
    # define what to do when starting, what to do in the process(yield), and what to do when stopping
    # init db when starting
    print(f"******** Starting {settings.APP_NAME}... ********")
    init_db()
    # skip creating if exists
    print("******** DB init finished ********")
    
    yield  # app currently running
    
    # clear resources when stopping
    print("******** app stopped ********")


# create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Hamster Game Backend API",
    version="0.1.0",
    lifespan=lifespan
)

# note: /docs, /redoc, /openapi.json are automaticlly created by fastAPI app. /health is definded by me.
# no more urls can be visited before db API is finished.


# -------- API routes --------
# health check API route
@app.get("/health")
# if request url /health, will return 200 ok
# cloud will automaticcly check this
def health_check():
    """health check"""
    return {"status": "ok", "app": settings.APP_NAME}

if settings.DEBUG:
    from app.api import debug
    app.include_router(debug.router, prefix="/api/debug", tags=["debug"])
# let app know what routes it can visit

# register/login API route
from app.api import auth
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# -------- API routes --------

# TODO: 注册各模块路由
# from app.api import auth, story, item, skin
# app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
# app.include_router(story.router, prefix="/api/story", tags=["Story"])
# app.include_router(item.router, prefix="/api/item", tags=["Item"])
# app.include_router(skin.router, prefix="/api/skin", tags=["Skin"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
