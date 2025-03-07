from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.database.db import Base

# SQLAlchemy模型

class XhsAuther(Base):
    """小红书作者信息表"""
    __tablename__ = "xhs_authers"
    
    auther_user_id = Column(String(64), primary_key=True, index=True, comment="作者用户ID")
    auther_nick_name = Column(String(128), nullable=True, comment="作者昵称")
    auther_avatar = Column(String(255), nullable=True, comment="作者头像URL")
    auther_home_page_url = Column(String(255), nullable=True, comment="作者主页URL")
    auther_desc = Column(Text, nullable=True, comment="作者简介")
    auther_interaction = Column(Integer, nullable=True, default=0, comment="互动数")
    auther_ip_location = Column(String(64), nullable=True, comment="作者所在地")
    auther_red_id = Column(String(64), nullable=True, comment="红书ID")
    auther_tags = Column(JSON, nullable=True, comment="作者标签")
    auther_fans = Column(Integer, nullable=True, default=0, comment="粉丝数量")
    auther_follows = Column(Integer, nullable=True, default=0, comment="关注数量")
    auther_gender = Column(String(16), nullable=True, comment="作者性别")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    notes = relationship("XhsNote", back_populates="auther")
    note_details = relationship("XhsNoteDetail", back_populates="auther")

    model_config = {
        "from_attributes": True
    }


class XhsNote(Base):
    """小红书笔记摘要表"""
    __tablename__ = "xhs_notes"
    
    note_id = Column(String(64), primary_key=True, index=True, comment="笔记ID")
    auther_user_id = Column(String(64), ForeignKey("xhs_authers.auther_user_id"), comment="作者用户ID")
    note_url = Column(String(255), nullable=False, comment="笔记URL")
    note_xsec_token = Column(String(255), nullable=True, comment="笔记xsec令牌")
    note_display_title = Column(String(255), nullable=True, comment="笔记标题")
    note_cover_url_pre = Column(String(255), nullable=True, comment="笔记预览封面URL")
    note_cover_url_default = Column(String(255), nullable=True, comment="笔记默认封面URL")
    note_cover_width = Column(Integer, nullable=True, comment="封面宽度")
    note_cover_height = Column(Integer, nullable=True, comment="封面高度")
    note_liked_count = Column(Integer, nullable=True, default=0, comment="点赞数")
    note_liked = Column(Boolean, nullable=True, default=False, comment="是否已点赞")
    note_card_type = Column(String(32), nullable=True, comment="笔记卡片类型")
    note_model_type = Column(String(32), nullable=True, comment="笔记模型类型")
    note_sticky = Column(Boolean, nullable=True, default=False, comment="是否置顶")
    
    # 作者相关的冗余字段
    auther_nick_name = Column(String(128), nullable=True, comment="作者昵称（冗余）")
    auther_avatar = Column(String(255), nullable=True, comment="作者头像URL（冗余）")
    auther_home_page_url = Column(String(255), nullable=True, comment="作者主页URL（冗余）")
    
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    auther = relationship("XhsAuther", back_populates="notes")
    details = relationship("XhsNoteDetail", back_populates="note", uselist=False)
    comments = relationship("XhsComment", back_populates="note")
    keyword_groups = relationship("XhsKeywordGroupNote", back_populates="note")

    model_config = {
        "from_attributes": True
    }


class XhsNoteDetail(Base):
    """小红书笔记详情表"""
    __tablename__ = "xhs_note_details"
    
    note_id = Column(String(64), ForeignKey("xhs_notes.note_id"), primary_key=True, comment="笔记ID")
    note_url = Column(String(255), nullable=False, comment="笔记URL")
    auther_user_id = Column(String(64), ForeignKey("xhs_authers.auther_user_id"), comment="作者用户ID")
    note_last_update_time = Column(DateTime, nullable=True, comment="最后更新时间")
    note_create_time = Column(DateTime, nullable=True, comment="创建时间")
    note_model_type = Column(String(32), nullable=True, comment="笔记模型类型")
    note_card_type = Column(String(32), nullable=True, comment="笔记卡片类型")
    note_display_title = Column(String(255), nullable=True, comment="笔记标题")
    note_desc = Column(Text, nullable=True, comment="笔记描述")
    comment_count = Column(Integer, nullable=True, default=0, comment="评论数")
    note_liked_count = Column(Integer, nullable=True, default=0, comment="点赞数")
    share_count = Column(Integer, nullable=True, default=0, comment="分享数")
    collected_count = Column(Integer, nullable=True, default=0, comment="收藏数")
    video_id = Column(String(64), nullable=True, comment="视频ID")
    video_h266_url = Column(String(255), nullable=True, comment="视频H266 URL")
    video_a1_url = Column(String(255), nullable=True, comment="视频a1 URL")
    video_h264_url = Column(String(255), nullable=True, comment="视频H264 URL")
    video_h265_url = Column(String(255), nullable=True, comment="视频H265 URL")
    note_duration = Column(Integer, nullable=True, comment="视频时长")
    note_image_list = Column(JSON, nullable=True, comment="笔记图片列表")
    note_tags = Column(JSON, nullable=True, comment="笔记标签")
    note_liked = Column(Boolean, nullable=True, default=False, comment="是否已点赞")
    collected = Column(Boolean, nullable=True, default=False, comment="是否已收藏")
    created_at = Column(DateTime, default=datetime.now, comment="记录创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="记录更新时间")
    
    # 关系
    note = relationship("XhsNote", back_populates="details")
    auther = relationship("XhsAuther", back_populates="note_details")


class XhsComment(Base):
    """小红书评论表"""
    __tablename__ = "xhs_comments"
    
    comment_id = Column(String(64), primary_key=True, index=True, comment="评论ID")
    note_id = Column(String(64), ForeignKey("xhs_notes.note_id"), comment="笔记ID")
    parent_comment_id = Column(String(64), nullable=True, comment="父评论ID")
    comment_user_id = Column(String(64), nullable=False, comment="评论用户ID")
    comment_user_image = Column(String(255), nullable=True, comment="评论者头像URL")
    comment_user_nickname = Column(String(128), nullable=True, comment="评论用户昵称")
    comment_user_home_page_url = Column(String(255), nullable=True, comment="评论者主页URL")
    comment_content = Column(Text, nullable=True, comment="评论内容")
    comment_like_count = Column(Integer, nullable=True, default=0, comment="点赞数")
    comment_sub_comment_count = Column(Integer, nullable=True, default=0, comment="子评论数量")
    comment_create_time = Column(DateTime, nullable=True, comment="评论创建时间")
    comment_liked = Column(Boolean, nullable=True, default=False, comment="是否已点赞")
    comment_show_tags = Column(JSON, nullable=True, comment="评论显示标签")
    comment_sub_comment_cursor = Column(String(64), nullable=True, comment="子评论分页游标")
    comment_sub_comment_has_more = Column(Boolean, nullable=True, default=False, comment="子评论是否有更多")
    created_at = Column(DateTime, default=datetime.now, comment="记录创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="记录更新时间")
    
    # 关系
    note = relationship("XhsNote", back_populates="comments")
    at_users = relationship("XhsCommentAtUser", back_populates="comment")


class XhsCommentAtUser(Base):
    """小红书评论@用户表"""
    __tablename__ = "xhs_comment_at_users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增ID")
    comment_id = Column(String(64), ForeignKey("xhs_comments.comment_id"), comment="评论ID")
    at_user_id = Column(String(64), nullable=False, comment="被@用户ID")
    at_user_nickname = Column(String(128), nullable=True, comment="被@用户昵称")
    at_user_home_page_url = Column(String(255), nullable=True, comment="被@用户主页")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    comment = relationship("XhsComment", back_populates="at_users")


class XhsKeywordGroup(Base):
    """小红书关键词群表"""
    __tablename__ = "xhs_keyword_groups"
    
    group_id = Column(Integer, primary_key=True, autoincrement=True, comment="群组ID")
    group_name = Column(String(100), nullable=True, comment="群组名称")
    keywords = Column(JSON, nullable=True, comment="关键词列表")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    notes = relationship("XhsKeywordGroupNote", back_populates="keyword_group")


class XhsKeywordGroupNote(Base):
    """小红书关键词群笔记关联表"""
    __tablename__ = "xhs_keyword_group_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增ID")
    group_id = Column(Integer, ForeignKey("xhs_keyword_groups.group_id"), comment="群组ID")
    note_id = Column(String(64), ForeignKey("xhs_notes.note_id"), comment="笔记ID")
    retrieved_at = Column(DateTime, default=datetime.now, comment="检索时间")
    
    # 关系
    keyword_group = relationship("XhsKeywordGroup", back_populates="notes")
    note = relationship("XhsNote", back_populates="keyword_groups")


# Pydantic模型用于API请求和响应

class XhsNoteItem(BaseModel):
    note_id: str
    note_url: Optional[str] = None
    note_xsec_token: Optional[str] = None
    auther_user_id: Optional[str] = None
    auther_nick_name: Optional[str] = None
    auther_avatar: Optional[str] = None
    auther_home_page_url: Optional[str] = None
    note_display_title: Optional[str] = None
    note_cover_url_pre: Optional[str] = None
    note_cover_url_default: Optional[str] = None
    note_cover_width: Optional[str] = None
    note_cover_height: Optional[str] = None
    note_liked_count: Optional[str] = None
    note_liked: Optional[bool] = None
    note_card_type: Optional[str] = None
    note_model_type: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class XhsSearchResponse(BaseModel):
    data: List[XhsNoteItem]
    msg: str = ""
    tips: Optional[str] = None
    code: int = 0

    model_config = {
        "from_attributes": True
    }


class SearchNoteRequest(BaseModel):
    req_info: Dict[str, Any]
    req_body: XhsSearchResponse


class XhsNoteDetailItem(BaseModel):
    note_last_update_time: Optional[str] = None
    note_model_type: Optional[str] = None
    video_h266_url: Optional[str] = None
    auther_avatar: Optional[str] = None
    note_card_type: Optional[str] = None
    note_desc: Optional[str] = None
    comment_count: Optional[str] = None
    note_liked_count: Optional[str] = None
    share_count: Optional[str] = None
    video_a1_url: Optional[str] = None
    auther_home_page_url: Optional[str] = None
    auther_user_id: Optional[str] = None
    collected_count: Optional[str] = None
    note_url: Optional[str] = None
    video_id: Optional[str] = None
    note_create_time: Optional[str] = None
    note_display_title: Optional[str] = None
    note_image_list: Optional[List[str]] = None
    note_tags: Optional[List[str]] = None
    video_h264_url: Optional[str] = None
    video_h265_url: Optional[str] = None
    auther_nick_name: Optional[str] = None
    note_duration: Optional[str] = None
    note_id: str
    note_liked: Optional[bool] = None
    collected: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }


class XhsNoteDetailData(BaseModel):
    note: XhsNoteDetailItem

    model_config = {
        "from_attributes": True
    }


class XhsNoteDetailResponse(BaseModel):
    data: XhsNoteDetailData
    msg: str = ""
    tips: Optional[str] = None
    code: int = 0

    model_config = {
        "from_attributes": True
    }


class NoteDetailRequest(BaseModel):
    req_info: Dict[str, Any]
    req_body: XhsNoteDetailResponse


class XhsCommentAtUserItem(BaseModel):
    at_user_id: str
    at_user_nickname: Optional[str] = None
    at_user_home_page_url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class XhsCommentSubItem(BaseModel):
    comment_id: str
    note_id: str
    comment_user_id: str
    comment_user_nickname: Optional[str] = None
    comment_user_image: Optional[str] = None
    comment_user_home_page_url: Optional[str] = None
    comment_content: Optional[str] = None
    comment_like_count: Optional[str] = None
    comment_sub_comment_count: Optional[str] = None
    comment_create_time: Optional[str] = None
    comment_liked: Optional[bool] = False
    comment_show_tags: Optional[List[str]] = None
    comment_sub_comment_cursor: Optional[str] = None
    comment_sub_comment_has_more: Optional[bool] = False
    comment_at_users: Optional[List[XhsCommentAtUserItem]] = Field(default_factory=list)
    comment_sub: Optional[List['XhsCommentSubItem']] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }


class XhsCommentItem(BaseModel):
    comment_id: str
    note_id: str
    comment_user_id: str
    comment_user_nickname: Optional[str] = None
    comment_user_image: Optional[str] = None
    comment_user_home_page_url: Optional[str] = None
    comment_content: Optional[str] = None
    comment_like_count: Optional[str] = None
    comment_sub_comment_count: Optional[str] = None
    comment_create_time: Optional[str] = None
    comment_liked: Optional[bool] = False
    comment_show_tags: Optional[List[str]] = None
    comment_sub_comment_cursor: Optional[str] = None
    comment_sub_comment_has_more: Optional[bool] = False
    comment_at_users: Optional[List[XhsCommentAtUserItem]] = Field(default_factory=list)
    comment_sub: Optional[List[XhsCommentSubItem]] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }


class XhsCommentsData(BaseModel):
    comments: List[XhsCommentItem]
    cursor: Optional[str] = None
    has_more: Optional[bool] = False

    model_config = {
        "from_attributes": True
    }


class XhsCommentsResponse(BaseModel):
    data: XhsCommentsData
    msg: str = ""
    tips: Optional[str] = None
    code: int = 0

    model_config = {
        "from_attributes": True
    }


class CommentsRequest(BaseModel):
    req_info: Dict[str, Any]
    req_body: XhsCommentsResponse


class XhsAutherInfo(BaseModel):
    user_link_url: Optional[str] = None
    desc: Optional[str] = None
    interaction: Optional[str] = None
    ip_location: Optional[str] = None
    red_id: Optional[str] = None
    user_id: str
    tags: Optional[List[str]] = None
    avatar: Optional[str] = None
    fans: Optional[str] = None
    follows: Optional[str] = None
    gender: Optional[str] = None
    nick_name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class XhsAutherNotesData(BaseModel):
    notes: List[XhsNoteItem]
    auther_info: XhsAutherInfo
    cursor: Optional[str] = None
    has_more: Optional[bool] = False

    model_config = {
        "from_attributes": True
    }


class XhsAutherNotesResponse(BaseModel):
    data: XhsAutherNotesData
    msg: str = ""
    tips: Optional[str] = None
    code: int = 0

    model_config = {
        "from_attributes": True
    }


class AutherNotesRequest(BaseModel):
    req_info: Dict[str, Any]
    req_body: XhsAutherNotesResponse 