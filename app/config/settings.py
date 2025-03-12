import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Settings(BaseSettings):
    # 应用设置
    APP_NAME: str = "MasterFlow"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # 数据库设置
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "masterflow")
    
    # 安全设置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # coze api
    COZE_API_TOKEN: str = os.getenv("COZE_API_TOKEN", "your-secret-key-here")
    
    # 小红书设置
    XHS_COOKIE: str = os.getenv("XHS_COOKIE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建设置实例
settings = Settings() 