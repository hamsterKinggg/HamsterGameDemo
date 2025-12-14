"""
仓鼠剧情互动游戏 - 后端入口
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时：初始化数据库
    print(f"正在启动 {settings.APP_NAME}...")
    init_db()
    print("数据库初始化完成")
    
    yield  # 应用运行中
    
    # 关闭时：清理资源（如果需要）
    print("应用关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    description="仓鼠剧情互动游戏后端 API",
    version="0.1.0",
    lifespan=lifespan
)


# 健康检查接口
@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok", "app": settings.APP_NAME}


# TODO: 注册各模块路由
# from app.api import auth, story, item, skin
# app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
# app.include_router(story.router, prefix="/api/story", tags=["剧情"])
# app.include_router(item.router, prefix="/api/item", tags=["道具"])
# app.include_router(skin.router, prefix="/api/skin", tags=["皮肤"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
