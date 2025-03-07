from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database.db import get_db
from app.api import router
from app.openapi import routes as openapi_routes

# 创建FastAPI应用实例
app = FastAPI(
    title="MasterFlow API",
    description="提供网络请求服务并与MySQL数据库交互的API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 实际生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router.router)
app.include_router(openapi_routes.router, prefix="/openapi")

@app.get("/")
async def root():
    return {"message": "欢迎使用MasterFlow API服务"}

@app.get("/health")
async def health_check():
    return {"status": "健康", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 