from fastapi import APIRouter
from app.api import users, items, auth

router = APIRouter(prefix="/api")

# 注册各个模块的路由
router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(users.router, prefix="/users", tags=["用户"])
router.include_router(items.router, prefix="/items", tags=["物品"]) 