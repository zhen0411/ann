from fastapi import APIRouter
from app.api.v1.endpoints import auth, projects, media, annotations

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(projects.router, prefix="/projects", tags=["项目管理"])
api_router.include_router(media.router, prefix="/media", tags=["媒体文件"])
api_router.include_router(annotations.router, prefix="/annotations", tags=["标注"])