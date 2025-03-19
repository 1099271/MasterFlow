from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.database.db import Base

class LlmConfiguration(Base):
    """LLM配置表"""
    __tablename__ = "llm_configurations"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    config_alias = Column(String(128), nullable=False, unique=True, comment="配置别名")
    model_name = Column(String(128), nullable=False, comment="模型名称")
    parameter_size = Column(String(64), nullable=False, comment="模型参数大小")
    temperature = Column(DECIMAL(3,2), nullable=True, comment="温度设置")
    top_p = Column(DECIMAL(3,2), nullable=True)
    max_tokens = Column(Integer, nullable=True)
    model_type = Column(String(32), nullable=True)
    other_params = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

class LlmNoteDiagnosis(Base):
    """LLM笔记诊断表"""
    __tablename__ = "llm_note_diagnosis"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键")
    note_id = Column(String(64), nullable=False, index=True, comment="笔记ID")
    llm_name = Column(String(128), nullable=False, comment="LLM模型名称")
    geo_tags = Column(JSON, nullable=True, comment="地理位置标签")
    cultural_tags = Column(JSON, nullable=True, comment="文化元素标签")
    other_tags = Column(JSON, nullable=True, comment="其他标签")
    user_gender = Column(String(16), nullable=True, comment="用户性别")
    user_age_range = Column(String(64), nullable=True, comment="年龄区间")
    user_location = Column(String(128), nullable=True, comment="地理位置")
    user_tags = Column(JSON, nullable=True, comment="用户标签")
    post_summary = Column(JSON, nullable=True, comment="帖子摘要")
    post_publish_time = Column(String(64), nullable=True, comment="发布时间")
    content_tendency = Column(String(16), nullable=True, comment="内容倾向")
    content_tendency_reason = Column(JSON, nullable=True, comment="倾向原因")
    has_visited = Column(Boolean, nullable=True, comment="是否去过")
    diagnosed_at = Column(DateTime, default=datetime.now, comment="诊断时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")