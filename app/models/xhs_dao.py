from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.models.xhs_models import (
    XhsAuther, XhsNote, XhsKeywordGroup, XhsKeywordGroupNote, XhsNoteDetailResponse,
    XhsSearchResponse, XhsNoteDetail, XhsComment, XhsCommentAtUser,
    XhsTopicDiscussion, XhsTopicsResponse, XhsCommentsResponse, XhsCommentItem, XhsCommentAtUserItem,
    XhsAutherNotesResponse
)
from datetime import datetime
import json
import traceback
import uuid
import sys
from app.utils.logger import get_logger, info, warning, error, debug

# 获取当前模块的日志器
logger = get_logger(__name__)
class XhsDAO:
    """小红书数据访问对象"""
    
    @staticmethod
    def get_or_create_auther(db: Session, auther_data: Dict[str, Any]) -> XhsAuther:
        """获取或创建作者记录"""
        auther_user_id = auther_data.get("auther_user_id")
        if not auther_user_id:
            info(f"警告：作者数据中缺少auther_user_id: {auther_data}")
            return None
        
        try:
            # 尝试查找作者
            auther = db.query(XhsAuther).filter(XhsAuther.auther_user_id == auther_user_id).first()
            
            # 如果作者不存在，创建新的作者记录
            if not auther:
                info(f"创建新作者: {auther_user_id}")
                auther = XhsAuther(
                    auther_user_id=auther_user_id,
                    auther_nick_name=auther_data.get("auther_nick_name"),
                    auther_avatar=auther_data.get("auther_avatar"),
                    auther_home_page_url=auther_data.get("auther_home_page_url"),
                    auther_desc=auther_data.get("auther_desc"),
                    auther_interaction=auther_data.get("auther_interaction"),
                    auther_ip_location=auther_data.get("auther_ip_location"),
                    auther_red_id=auther_data.get("auther_red_id"),
                    auther_tags=auther_data.get("auther_tags"),
                    auther_fans=auther_data.get("auther_fans"),
                    auther_follows=auther_data.get("auther_follows"),
                    auther_gender=auther_data.get("auther_gender")
                )
                db.add(auther)
                db.flush()
                info(f"新作者创建成功: {auther_user_id}")
            else:
                info(f"更新现有作者: {auther_user_id}")
                # 更新作者信息
                auther.auther_nick_name = auther_data.get("auther_nick_name", auther.auther_nick_name)
                auther.auther_avatar = auther_data.get("auther_avatar", auther.auther_avatar)
                auther.auther_home_page_url = auther_data.get("auther_home_page_url", auther.auther_home_page_url)
                auther.auther_desc = auther_data.get("auther_desc", auther.auther_desc)
                auther.auther_interaction = auther_data.get("auther_interaction", auther.auther_interaction)
                auther.auther_ip_location = auther_data.get("auther_ip_location", auther.auther_ip_location)
                auther.auther_red_id = auther_data.get("auther_red_id", auther.auther_red_id)
                auther.auther_tags = auther_data.get("auther_tags", auther.auther_tags)
                auther.auther_fans = auther_data.get("auther_fans", auther.auther_fans)
                auther.auther_follows = auther_data.get("auther_follows", auther.auther_follows)
                auther.auther_gender = auther_data.get("auther_gender", auther.auther_gender)
                auther.updated_at = datetime.now()
                info(f"作者信息更新成功: {auther_user_id}")
                
            return auther
            
        except Exception as e:
            info(f"处理作者数据时出错 {auther_user_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_or_create_note(db: Session, note_data: Dict[str, Any]) -> XhsNote:
        """获取或创建笔记记录"""
        note_id = note_data.get("note_id")
        if not note_id:
            return None
        
        # 尝试查找笔记
        note = db.query(XhsNote).filter(XhsNote.note_id == note_id).first()
        
        # 如果笔记不存在，创建新的笔记记录
        if not note:
            note = XhsNote(
                note_id=note_id,
                auther_user_id=note_data.get("auther_user_id"),
                note_url=note_data.get("note_url"),
                note_xsec_token=note_data.get("note_xsec_token"),
                note_display_title=note_data.get("note_display_title"),
                note_cover_url_pre=note_data.get("note_cover_url_pre"),
                note_cover_url_default=note_data.get("note_cover_url_default"),
                note_cover_width=note_data.get("note_cover_width"),
                note_cover_height=note_data.get("note_cover_height"),
                note_liked_count=note_data.get("note_liked_count"),
                note_liked=note_data.get("note_liked"),
                note_card_type=note_data.get("note_card_type"),
                note_model_type=note_data.get("note_model_type"),
                # 添加作者相关的冗余字段
                auther_nick_name=note_data.get("auther_nick_name"),
                auther_avatar=note_data.get("auther_avatar"),
                auther_home_page_url=note_data.get("auther_home_page_url")
            )
            db.add(note)
            db.flush()
        else:
            # 更新笔记信息
            note.note_url = note_data.get("note_url", note.note_url)
            note.note_xsec_token = note_data.get("note_xsec_token", note.note_xsec_token)
            note.note_display_title = note_data.get("note_display_title", note.note_display_title)
            note.note_cover_url_pre = note_data.get("note_cover_url_pre", note.note_cover_url_pre)
            note.note_cover_url_default = note_data.get("note_cover_url_default", note.note_cover_url_default)
            note.note_cover_width = note_data.get("note_cover_width", note.note_cover_width)
            note.note_cover_height = note_data.get("note_cover_height", note.note_cover_height)
            note.note_liked_count = note_data.get("note_liked_count", note.note_liked_count)
            note.note_liked = note_data.get("note_liked", note.note_liked)
            note.note_card_type = note_data.get("note_card_type", note.note_card_type)
            note.note_model_type = note_data.get("note_model_type", note.note_model_type)
            # 更新作者相关的冗余字段
            note.auther_nick_name = note_data.get("auther_nick_name", note.auther_nick_name)
            note.auther_avatar = note_data.get("auther_avatar", note.auther_avatar)
            note.auther_home_page_url = note_data.get("auther_home_page_url", note.auther_home_page_url)
            note.updated_at = datetime.now()
            
        return note
    
    @staticmethod
    def get_or_create_keyword_group(db: Session, keywords: str, group_name: Optional[str] = None) -> XhsKeywordGroup:
        """获取或创建关键词群组"""
        
        
        try:
            # 尝试查找关键词群组（精确匹配关键词列表）
            keyword_group = db.query(XhsKeywordGroup).filter(
                XhsKeywordGroup.keywords == keywords
            ).first()
            
            # 如果关键词群组不存在，创建新的关键词群组
            if not keyword_group:
                # 生成唯一的群组名称
                unique_group_name = group_name or f"关键词群组-{uuid.uuid4().hex[:8]}"
                
                keyword_group = XhsKeywordGroup(
                    group_name=unique_group_name,
                    keywords=keywords  # 使用JSON字符串而不是原始列表
                )
                db.add(keyword_group)
                db.flush()
                info(f"创建新的关键词群组: {unique_group_name}, 关键词: {keywords}")
            else:
                info(f"找到现有关键词群组: {keyword_group.group_name}, ID: {keyword_group.group_id}")
                
            return keyword_group
            
        except Exception as e:
            error(f"创建或获取关键词群组时出错: {str(e)}")
            # 创建一个临时的关键词群组对象，不保存到数据库
            # 这样即使出错，后续代码也能继续执行
            temp_group = XhsKeywordGroup(
                group_id=-1,  # 使用一个不可能的ID
                group_name="临时关键词群组",
                keywords=keywords
            )
            return temp_group
    
    @staticmethod
    def associate_note_with_keyword_group(db: Session, note_id: str, group_id: int) -> XhsKeywordGroupNote:
        """将笔记与关键词群组关联"""
        # 检查关联是否已存在
        association = db.query(XhsKeywordGroupNote).filter(
            XhsKeywordGroupNote.note_id == note_id,
            XhsKeywordGroupNote.group_id == group_id
        ).first()
        
        # 如果关联不存在，创建新的关联
        if not association:
            association = XhsKeywordGroupNote(
                note_id=note_id,
                group_id=group_id
            )
            db.add(association)
            db.flush()
        else:
            # 更新检索时间
            association.retrieved_at = datetime.now()
            
        return association
    
    @staticmethod
    def store_search_results(db: Session, req_info: Dict[str, Any], search_response: XhsSearchResponse) -> List[XhsNote]:
        """存储搜索结果数据，确保幂等性操作"""
        stored_notes = []
        
        # 在开始前确保会话是干净的
        db.rollback()
        
        try:
            # 1. 首先收集所有需要处理的note_ids和auther_ids
            note_ids = [note.note_id for note in search_response.data]
            auther_ids = [note.auther_user_id for note in search_response.data]
            
            info(f"开始处理 {len(note_ids)} 条笔记数据")
            
            # 2. 批量查询已存在的笔记和作者
            existing_notes = {}
            existing_authers = {}
            
            # 查询笔记
            try:
                existing_notes = {
                    note.note_id: note 
                    for note in db.query(XhsNote).filter(XhsNote.note_id.in_(note_ids)).all()
                }
                info(f"找到 {len(existing_notes)} 条已存在的笔记")
            except Exception as e:
                error(f"查询笔记信息时出错: {str(e)}")
            
            # 查询作者
            try:
                existing_authers = {
                    auther.auther_user_id: auther 
                    for auther in db.query(XhsAuther).filter(XhsAuther.auther_user_id.in_(auther_ids)).all()
                }
                info(f"找到 {len(existing_authers)} 个已存在的作者")
            except Exception as e:
                error(f"查询作者信息时出错: {str(e)}")
                
                # 尝试单独查询每个作者，以便找出问题所在
                for auther_id in auther_ids:
                    try:
                        auther = db.query(XhsAuther).filter(XhsAuther.auther_user_id == auther_id).first()
                        if auther:
                            existing_authers[auther.auther_user_id] = auther
                    except Exception as e2:
                        error(f"查询单个作者 {auther_id} 时出错: {str(e2)}")
            
            # 3. 获取或创建关键词群组
            keyword_group = None
            existing_associations = set()
            
            keywords = [req_info.get("keywords")] if req_info.get("keywords") else []
            if keywords:
                # 确保关键词是字符串
                # keywords = [str(k) for k in keywords if k]
                try:
                    keyword_group = XhsDAO.get_or_create_keyword_group(db, keywords)
                    
                    # 只有当关键词群组创建成功且有有效ID时才查询关联关系
                    if keyword_group and keyword_group.group_id > 0:
                        # 批量查询已存在的关联关系
                        existing_associations = {
                            note_id 
                            for (note_id,) in db.query(XhsKeywordGroupNote.note_id).filter(
                                XhsKeywordGroupNote.group_id == keyword_group.group_id,
                                XhsKeywordGroupNote.note_id.in_(note_ids)
                            ).all()
                        }
                        info(f"关键词群组: {keywords}, 已存在关联关系数量: {len(existing_associations)}")
                except Exception as e:
                    error(f"处理关键词群组时出错: {str(e)}")
                    keyword_group = None
                    existing_associations = set()
            
            # 4. 处理每个笔记
            for note_item in search_response.data:
                try:
                    # 处理作者信息
                    auther_data = {
                        "auther_user_id": str(note_item.auther_user_id) if note_item.auther_user_id else "",
                        "auther_nick_name": str(note_item.auther_nick_name) if note_item.auther_nick_name else "",
                        "auther_avatar": str(note_item.auther_avatar) if note_item.auther_avatar else "",
                        "auther_home_page_url": str(note_item.auther_home_page_url) if note_item.auther_home_page_url else "",
                        "auther_desc": '',  # 添加默认值
                        "auther_interaction": 0,  # 根据数据库结构设置默认值为0
                        "auther_ip_location": None,
                        "auther_red_id": None,
                        "auther_tags": None,
                        "auther_fans": 0,
                        "auther_follows": 0,
                        "auther_gender": None
                    }
                    
                    # 获取或更新作者
                    auther = existing_authers.get(note_item.auther_user_id)
                    if auther:
                        # 更新现有作者信息
                        for key, value in auther_data.items():
                            if hasattr(auther, key):
                                setattr(auther, key, value)
                        auther.updated_at = datetime.now()
                        logger.debug(f"更新作者信息: {auther.auther_user_id}")
                    else:
                        # 创建新作者
                        auther = XhsAuther(**auther_data)
                        db.add(auther)
                        existing_authers[auther.auther_user_id] = auther
                        logger.debug(f"创建新作者: {auther.auther_user_id}")
                    
                    # 准备笔记数据（确保数值类型正确）
                    note_data = {
                        "note_id": str(note_item.note_id) if note_item.note_id else "",
                        "auther_user_id": str(note_item.auther_user_id) if note_item.auther_user_id else "",
                        "note_url": str(note_item.note_url) if note_item.note_url else "",
                        "note_xsec_token": str(note_item.note_xsec_token) if note_item.note_xsec_token else "",
                        "note_display_title": str(note_item.note_display_title) if note_item.note_display_title else "",
                        "note_cover_url_pre": str(note_item.note_cover_url_pre) if note_item.note_cover_url_pre else "",
                        "note_cover_url_default": str(note_item.note_cover_url_default) if note_item.note_cover_url_default else "",
                        "note_cover_width": int(note_item.note_cover_width) if note_item.note_cover_width and str(note_item.note_cover_width).isdigit() else None,
                        "note_cover_height": int(note_item.note_cover_height) if note_item.note_cover_height and str(note_item.note_cover_height).isdigit() else None,
                        "note_liked_count": int(note_item.note_liked_count) if note_item.note_liked_count and str(note_item.note_liked_count).isdigit() else 0,
                        "note_liked": bool(note_item.note_liked) if note_item.note_liked is not None else False,
                        "note_card_type": str(note_item.note_card_type) if note_item.note_card_type else "",
                        "note_model_type": str(note_item.note_model_type) if note_item.note_model_type else "",
                        "auther_nick_name": str(note_item.auther_nick_name) if note_item.auther_nick_name else "",
                        "auther_avatar": str(note_item.auther_avatar) if note_item.auther_avatar else "",
                        "auther_home_page_url": str(note_item.auther_home_page_url) if note_item.auther_home_page_url else ""
                    }
                    
                    # 获取或更新笔记
                    note = existing_notes.get(note_item.note_id)
                    if note:
                        # 更新现有笔记
                        for key, value in note_data.items():
                            if hasattr(note, key):
                                setattr(note, key, value)
                        note.updated_at = datetime.now()
                        logger.debug(f"更新笔记: {note.note_id}")
                    else:
                        # 创建新笔记
                        note = XhsNote(**note_data)
                        db.add(note)
                        existing_notes[note.note_id] = note
                        logger.debug(f"创建新笔记: {note.note_id}")
                    
                    # 同步存储或更新笔记详情
                    note_detail_data = {
                        "note_id": note.note_id,
                        "note_url": note.note_url,  # 从笔记中获取URL
                        "auther_user_id": note.auther_user_id,
                        "note_last_update_time": datetime.now(),
                        "note_create_time": datetime.now(),
                        "note_model_type": note.note_model_type,  # 从笔记中获取模型类型
                        "note_card_type": note.note_card_type,  # 从笔记中获取卡片类型
                        "note_display_title": note.note_display_title,  # 从笔记中获取标题
                        "note_desc": None,
                        "comment_count": 0,
                        "note_liked_count": note.note_liked_count,  # 从笔记中获取点赞数
                        "share_count": 0,
                        "collected_count": 0,
                        "video_id": None,
                        "video_h266_url": None,
                        "video_a1_url": None,
                        "video_h264_url": None,
                        "video_h265_url": None,
                        "note_duration": None,
                        "note_image_list": json.dumps(note_data.note_image_list, ensure_ascii=False) if note_data.note_image_list and len(note_data.note_image_list) > 0 else None,
                        "note_tags": json.dumps(note_data.note_tags, ensure_ascii=False) if note_data.note_tags and len(note_data.note_tags) > 0 else None,
                        "note_liked": note.note_liked,  # 从笔记中获取是否点赞
                        "collected": False
                    }

                    # 获取或更新笔记详情
                    note_detail = db.query(XhsNoteDetail).filter(XhsNoteDetail.note_id == note.note_id).first()
                    if note_detail:
                        # 更新现有笔记详情
                        for key, value in note_detail_data.items():
                            if hasattr(note_detail, key):
                                setattr(note_detail, key, value)
                        note_detail.updated_at = datetime.now()
                        logger.debug(f"更新笔记详情: {note_detail.note_id}")
                    else:
                        # 创建新笔记详情
                        note_detail = XhsNoteDetail(**note_detail_data)
                        db.add(note_detail)
                        logger.debug(f"创建新笔记详情: {note_detail.note_id}")

                    stored_notes.append(note)
                    
                    # 处理关键词群组关联
                    if keywords and keyword_group and keyword_group.group_id > 0 and note.note_id not in existing_associations:
                        try:
                            association = XhsKeywordGroupNote(
                                note_id=note.note_id,
                                group_id=keyword_group.group_id,  # 使用整数类型，不需要转换为字符串
                                retrieved_at=datetime.now()
                            )
                            db.add(association)
                            existing_associations.add(note.note_id)
                            logger.debug(f"创建关键词关联: {note.note_id} -> {keywords}")
                        except Exception as e:
                            error(f"创建关键词关联时出错: {str(e)}")
                
                except Exception as e:
                    error(f"处理笔记时出错 {getattr(note_item, 'note_id', '未知')}: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}")
                    continue
            
            # 5. 提交事务
            try:
                # 每100条记录提交一次，避免事务过大
                db.flush()
                db.commit()
                info(f"成功处理并存储 {len(stored_notes)} 条笔记数据")
            except Exception as e:
                db.rollback()
                error_detail = f"提交事务时出错: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
                error(error_detail)
                # 不抛出异常，而是返回已处理的笔记
                warning("由于事务提交错误，可能有部分数据未能成功存储")
            
        except Exception as e:
            db.rollback()
            error_detail = f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
            error(f"存储过程中发生错误: {error_detail}")
            raise
        
        return stored_notes

    @staticmethod
    def store_note_detail(db: Session, req_info: Dict[str, Any], note_detail_response: 'XhsNoteDetailResponse') -> XhsNote:
        """存储笔记详情数据，确保幂等性操作"""
        
        
        # 在开始前确保会话是干净的
        db.rollback()
        
        try:
            # 获取笔记详情数据
            note_data = note_detail_response.data.note
            
            if not note_data or not note_data.note_id:
                warning("请求体中缺少有效的笔记详情数据")
                return None
            # 处理作者信息
            auther_data = {
                "auther_user_id": str(note_data.auther_user_id) if note_data.auther_user_id else "",
                "auther_nick_name": str(note_data.auther_nick_name) if note_data.auther_nick_name else "",
                "auther_avatar": str(note_data.auther_avatar) if note_data.auther_avatar else "",
                "auther_home_page_url": str(note_data.auther_home_page_url) if note_data.auther_home_page_url else "",
                "auther_desc": '',  # 添加默认值
                "auther_interaction": 0,  # 根据数据库结构设置默认值为0
                "auther_ip_location": None,
                "auther_red_id": None,
                "auther_tags": None,
                "auther_fans": 0,
                "auther_follows": 0,
                "auther_gender": None
            }
            
            # 获取或更新作者
            auther = XhsDAO.get_or_create_auther(db, auther_data)
            
            # 准备笔记基本数据
            note_basic_data = {
                "note_id": str(note_data.note_id),
                "auther_user_id": str(note_data.auther_user_id) if note_data.auther_user_id else "",
                "note_url": str(note_data.note_url) if note_data.note_url else "",
                "note_xsec_token": str(note_data.note_xsec_token) if hasattr(note_data, 'note_xsec_token') else "",
                "note_display_title": str(note_data.note_display_title) if note_data.note_display_title else "",
                "note_cover_url_pre": str(note_data.note_cover_url_pre) if hasattr(note_data, 'note_cover_url_pre') else "",
                "note_cover_url_default": str(note_data.note_cover_url_default) if hasattr(note_data, 'note_cover_url_default') else "",
                "note_cover_width": int(note_data.note_cover_width) if hasattr(note_data, 'note_cover_width') and str(note_data.note_cover_width).isdigit() else None,
                "note_cover_height": int(note_data.note_cover_height) if hasattr(note_data, 'note_cover_height') and str(note_data.note_cover_height).isdigit() else None,
                "note_liked_count": int(note_data.note_liked_count) if note_data.note_liked_count and str(note_data.note_liked_count).isdigit() else 0,
                "note_liked": bool(note_data.note_liked) if note_data.note_liked is not None else False,
                "note_card_type": str(note_data.note_card_type) if note_data.note_card_type else "",
                "note_model_type": str(note_data.note_model_type) if note_data.note_model_type else "",
                "auther_nick_name": str(note_data.auther_nick_name) if note_data.auther_nick_name else "",
                "auther_avatar": str(note_data.auther_avatar) if note_data.auther_avatar else "",
                "auther_home_page_url": str(note_data.auther_home_page_url) if note_data.auther_home_page_url else ""
            }
            
            # 获取或更新笔记基本信息
            note = XhsDAO.get_or_create_note(db, note_basic_data)
            
            # 处理笔记详情数据
            # 转换日期时间字符串为datetime对象
            note_create_time = None
            note_last_update_time = None
            
            if note_data.note_create_time:
                try:
                    note_create_time = datetime.strptime(note_data.note_create_time, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    warning(f"解析笔记创建时间出错: {str(e)}")
                    note_create_time = datetime.now()
            else:
                note_create_time = datetime.now()
                
            if note_data.note_last_update_time:
                try:
                    note_last_update_time = datetime.strptime(note_data.note_last_update_time, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    warning(f"解析笔记更新时间出错: {str(e)}")
                    note_last_update_time = datetime.now()
            else:
                note_last_update_time = datetime.now()
            
            # 准备笔记详情数据
            note_detail_data = {
                "note_id": note.note_id,
                "note_url": note.note_url,
                "auther_user_id": note.auther_user_id,
                "note_last_update_time": note_last_update_time,
                "note_create_time": note_create_time,
                "note_model_type": str(note_data.note_model_type) if note_data.note_model_type else "",
                "note_card_type": str(note_data.note_card_type) if note_data.note_card_type else "",
                "note_display_title": str(note_data.note_display_title) if note_data.note_display_title else "",
                "note_desc": str(note_data.note_desc) if note_data.note_desc else "",
                "comment_count": int(note_data.comment_count) if note_data.comment_count and str(note_data.comment_count).isdigit() else 0,
                "note_liked_count": int(note_data.note_liked_count) if note_data.note_liked_count and str(note_data.note_liked_count).isdigit() else 0,
                "share_count": int(note_data.share_count) if note_data.share_count and str(note_data.share_count).isdigit() else 0,
                "collected_count": int(note_data.collected_count) if note_data.collected_count and str(note_data.collected_count).isdigit() else 0,
                "video_id": str(note_data.video_id) if note_data.video_id else None,
                "video_h266_url": str(note_data.video_h266_url) if note_data.video_h266_url else None,
                "video_a1_url": str(note_data.video_a1_url) if note_data.video_a1_url else None,
                "video_h264_url": str(note_data.video_h264_url) if note_data.video_h264_url else None,
                "video_h265_url": str(note_data.video_h265_url) if note_data.video_h265_url else None,
                "note_duration": int(note_data.note_duration) if note_data.note_duration and str(note_data.note_duration).isdigit() else None,
                "note_image_list": json.dumps(note_data.note_image_list, ensure_ascii=False) if note_data.note_image_list and len(note_data.note_image_list) > 0 else None,
                "note_tags": json.dumps(note_data.note_tags, ensure_ascii=False) if note_data.note_tags and len(note_data.note_tags) > 0 else None,
                "note_liked": bool(note_data.note_liked) if note_data.note_liked is not None else False,
                "collected": bool(note_data.collected) if note_data.collected is not None else False
            }
            
            # 获取或更新笔记详情
            note_detail = db.query(XhsNoteDetail).filter(XhsNoteDetail.note_id == note.note_id).first()
            if note_detail:
                # 更新现有笔记详情
                for key, value in note_detail_data.items():
                    if hasattr(note_detail, key):
                        setattr(note_detail, key, value)
                note_detail.updated_at = datetime.now()
                logger.debug(f"更新笔记详情: {note_detail.note_id}")
            else:
                # 创建新笔记详情
                note_detail = XhsNoteDetail(**note_detail_data)
                db.add(note_detail)
                logger.debug(f"创建新笔记详情: {note_detail.note_id}")
            
            # 提交事务
            try:
                db.flush()
                db.commit()
                info(f"成功处理并存储笔记详情数据，笔记ID: {note.note_id}")
                return note
            except Exception as e:
                db.rollback()
                error_detail = f"提交事务时出错: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
                error(error_detail)
                warning("由于事务提交错误，可能有部分数据未能成功存储")
                return None
                
        except Exception as e:
            db.rollback()
            error_detail = f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
            error(f"存储笔记详情过程中发生错误: {error_detail}")
            raise 

    @staticmethod
    def store_comments(db: Session, req_info: Dict[str, Any], comments_response: 'XhsCommentsResponse') -> List[XhsComment]:
        """存储评论数据，确保幂等性操作"""
        
        
        # 在开始前确保会话是干净的
        db.rollback()
        
        try:
            # 获取评论数据
            comments_data = comments_response.data.comments
            
            if not comments_data:
                warning("请求体中缺少有效的评论数据")
                return []
                
            info(f"开始处理评论数据，共 {len(comments_data)} 条评论")
            
            # 收集所有评论ID和用户ID
            comment_ids = []
            user_ids = []
            
            for comment in comments_data:
                comment_ids.append(comment.comment_id)
                user_ids.append(comment.comment_user_id)
                
                # 收集子评论的ID和用户ID
                for sub_comment in comment.comment_sub:
                    comment_ids.append(sub_comment.comment_id)
                    user_ids.append(sub_comment.comment_user_id)
            
            # 去重
            comment_ids = list(set(comment_ids))
            user_ids = list(set(user_ids))
            
            info(f"共有 {len(comment_ids)} 条不重复评论，{len(user_ids)} 个不重复用户")
            
            # 查询已存在的评论
            existing_comments = {
                comment.comment_id: comment 
                for comment in db.query(XhsComment).filter(XhsComment.comment_id.in_(comment_ids)).all()
            }
            
            info(f"找到 {len(existing_comments)} 条已存在的评论")
            
            # 存储评论数据
            stored_comments = []
            
            for comment_item in comments_data:
                try:
                    # 处理主评论
                    comment = XhsDAO._process_comment(db, comment_item, existing_comments)
                    
                    # 处理@用户
                    if comment_item.comment_at_users:
                        for at_user in comment_item.comment_at_users:
                            XhsDAO._process_comment_at_user(db, comment.comment_id, at_user)
                    
                    # 处理子评论
                    if comment_item.comment_sub:
                        for sub_comment_item in comment_item.comment_sub:
                            sub_comment = XhsDAO._process_comment(db, sub_comment_item, existing_comments, parent_id=comment.comment_id)
                            
                            # 处理子评论的@用户
                            if sub_comment_item.comment_at_users:
                                for at_user in sub_comment_item.comment_at_users:
                                    XhsDAO._process_comment_at_user(db, sub_comment.comment_id, at_user)
                    
                    stored_comments.append(comment)
                    
                except Exception as e:
                    error(f"处理评论时出错 {comment_item.comment_id}: {str(e)}")
                    continue
            
            # 提交事务
            try:
                db.flush()
                db.commit()
                info(f"成功处理并存储 {len(stored_comments)} 条评论数据")
            except Exception as e:
                db.rollback()
                error_detail = f"提交事务时出错: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
                error(error_detail)
                warning("由于事务提交错误，可能有部分数据未能成功存储")
            
            return stored_comments
            
        except Exception as e:
            db.rollback()
            error_detail = f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
            error(f"存储评论过程中发生错误: {error_detail}")
            raise
    
    @staticmethod
    def _process_comment(db: Session, comment_item: 'XhsCommentItem', existing_comments: Dict[str, XhsComment], parent_id: Optional[str] = None) -> XhsComment:
        """处理单条评论数据"""
        
        
        # 检查评论是否已存在
        comment = existing_comments.get(comment_item.comment_id)
        
        # 转换评论创建时间
        comment_create_time = None
        if comment_item.comment_create_time:
            try:
                comment_create_time = datetime.strptime(comment_item.comment_create_time, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                warning(f"解析评论创建时间出错: {str(e)}")
                comment_create_time = datetime.now()
        else:
            comment_create_time = datetime.now()
        
        # 转换评论标签
        comment_show_tags = None
        if comment_item.comment_show_tags:
            try:
                comment_show_tags = json.dumps(comment_item.comment_show_tags)
            except Exception as e:
                warning(f"转换评论标签出错: {str(e)}")
        
        if not comment:
            # 创建新评论
            comment = XhsComment(
                comment_id=comment_item.comment_id,
                note_id=comment_item.note_id,
                parent_comment_id=parent_id,
                comment_user_id=comment_item.comment_user_id,
                comment_user_image=comment_item.comment_user_image,
                comment_user_nickname=comment_item.comment_user_nickname,
                comment_user_home_page_url=comment_item.comment_user_home_page_url,
                comment_content=comment_item.comment_content,
                comment_like_count=int(comment_item.comment_like_count) if comment_item.comment_like_count and str(comment_item.comment_like_count).isdigit() else 0,
                comment_sub_comment_count=int(comment_item.comment_sub_comment_count) if comment_item.comment_sub_comment_count and str(comment_item.comment_sub_comment_count).isdigit() else 0,
                comment_create_time=comment_create_time,
                comment_liked=comment_item.comment_liked,
                comment_show_tags=comment_show_tags,
                comment_sub_comment_cursor=comment_item.comment_sub_comment_cursor,
                comment_sub_comment_has_more=comment_item.comment_sub_comment_has_more
            )
            db.add(comment)
            db.flush()
            existing_comments[comment.comment_id] = comment
            logger.debug(f"创建新评论: {comment.comment_id}")
        else:
            # 更新现有评论
            comment.note_id = comment_item.note_id
            comment.parent_comment_id = parent_id
            comment.comment_user_id = comment_item.comment_user_id
            comment.comment_user_image = comment_item.comment_user_image
            comment.comment_user_nickname = comment_item.comment_user_nickname
            comment.comment_user_home_page_url = comment_item.comment_user_home_page_url
            comment.comment_content = comment_item.comment_content
            comment.comment_like_count = int(comment_item.comment_like_count) if comment_item.comment_like_count and str(comment_item.comment_like_count).isdigit() else 0
            comment.comment_sub_comment_count = int(comment_item.comment_sub_comment_count) if comment_item.comment_sub_comment_count and str(comment_item.comment_sub_comment_count).isdigit() else 0
            comment.comment_create_time = comment_create_time
            comment.comment_liked = comment_item.comment_liked
            comment.comment_show_tags = comment_show_tags
            comment.comment_sub_comment_cursor = comment_item.comment_sub_comment_cursor
            comment.comment_sub_comment_has_more = comment_item.comment_sub_comment_has_more
            comment.updated_at = datetime.now()
            logger.debug(f"更新评论: {comment.comment_id}")
        
        return comment
    
    @staticmethod
    def _process_comment_at_user(db: Session, comment_id: str, at_user_item: 'XhsCommentAtUserItem') -> XhsCommentAtUser:
        """处理评论@用户数据"""
        
        
        # 检查@用户关系是否已存在
        at_user = db.query(XhsCommentAtUser).filter(
            XhsCommentAtUser.comment_id == comment_id,
            XhsCommentAtUser.at_user_id == at_user_item.at_user_id
        ).first()
        
        if not at_user:
            # 创建新的@用户关系
            at_user = XhsCommentAtUser(
                comment_id=comment_id,
                at_user_id=at_user_item.at_user_id,
                at_user_nickname=at_user_item.at_user_nickname,
                at_user_home_page_url=at_user_item.at_user_home_page_url
            )
            db.add(at_user)
            db.flush()
            logger.debug(f"创建新的@用户关系: {comment_id} -> {at_user_item.at_user_id}")
        else:
            # 更新现有@用户关系
            at_user.at_user_nickname = at_user_item.at_user_nickname
            at_user.at_user_home_page_url = at_user_item.at_user_home_page_url
            logger.debug(f"更新@用户关系: {comment_id} -> {at_user_item.at_user_id}")
        
        return at_user 

    @staticmethod
    def store_auther_notes(db: Session, req_info: Dict[str, Any], auther_notes_response: 'XhsAutherNotesResponse') -> List[XhsNote]:
        """存储作者笔记数据，确保幂等性操作"""
        
        
        # 在开始前确保会话是干净的
        db.rollback()
        
        try:
            # 获取作者信息和笔记数据
            auther_info = auther_notes_response.data.auther_info
            notes_data = auther_notes_response.data.notes
            
            if not auther_info or not auther_info.user_id:
                warning("请求体中缺少有效的作者信息")
                return []
                
            info(f"开始处理作者笔记数据，作者ID: {auther_info.user_id}, 笔记数量: {len(notes_data)}")
            
            # 处理作者信息
            auther_data = {
                "auther_user_id": str(auther_info.user_id),
                "auther_nick_name": str(auther_info.nick_name) if auther_info.nick_name else "",
                "auther_avatar": str(auther_info.avatar) if auther_info.avatar else "",
                "auther_home_page_url": str(auther_info.user_link_url) if auther_info.user_link_url else "",
                "auther_desc": str(auther_info.desc) if auther_info.desc else "",
                "auther_interaction": int(auther_info.interaction) if auther_info.interaction and str(auther_info.interaction).isdigit() else 0,
                "auther_ip_location": str(auther_info.ip_location) if auther_info.ip_location else None,
                "auther_red_id": str(auther_info.red_id) if auther_info.red_id else None,
                "auther_tags": json.dumps(auther_info.tags, ensure_ascii=False) if auther_info.tags else None,
                "auther_fans": int(auther_info.fans) if auther_info.fans and str(auther_info.fans).isdigit() else 0,
                "auther_follows": int(auther_info.follows) if auther_info.follows and str(auther_info.follows).isdigit() else 0,
                "auther_gender": str(auther_info.gender) if auther_info.gender else None
            }
            
            # 获取或更新作者
            auther = XhsDAO.get_or_create_auther(db, auther_data)
            
            # 处理笔记数据
            stored_notes = []
            
            for note_item in notes_data:
                try:
                    # 准备笔记数据
                    note_data = {
                        "note_id": str(note_item.note_id),
                        "auther_user_id": str(auther_info.user_id),
                        "note_url": str(note_item.note_url) if note_item.note_url else "",
                        "note_xsec_token": str(note_item.note_xsec_token) if note_item.note_xsec_token else "",
                        "note_display_title": str(note_item.note_display_title) if note_item.note_display_title else "",
                        "note_cover_url_pre": str(note_item.note_cover_url_pre) if note_item.note_cover_url_pre else "",
                        "note_cover_url_default": str(note_item.note_cover_url_default) if note_item.note_cover_url_default else "",
                        "note_cover_width": int(note_item.note_cover_width) if note_item.note_cover_width and str(note_item.note_cover_width).isdigit() else None,
                        "note_cover_height": int(note_item.note_cover_height) if note_item.note_cover_height and str(note_item.note_cover_height).isdigit() else None,
                        "note_liked_count": int(note_item.note_liked_count) if note_item.note_liked_count and str(note_item.note_liked_count).isdigit() else 0,
                        "note_liked": bool(note_item.note_liked) if note_item.note_liked is not None else False,
                        "note_card_type": str(note_item.note_card_type) if note_item.note_card_type else "",
                        "note_model_type": str(note_item.note_model_type) if note_item.note_model_type else "",
                        "auther_nick_name": str(auther_info.nick_name) if auther_info.nick_name else "",
                        "auther_avatar": str(auther_info.avatar) if auther_info.avatar else "",
                        "auther_home_page_url": str(auther_info.user_link_url) if auther_info.user_link_url else ""
                    }
                    
                    # 获取或更新笔记
                    note = XhsDAO.get_or_create_note(db, note_data)
                    stored_notes.append(note)
                    
                except Exception as e:
                    error(f"处理笔记时出错 {note_item.note_id}: {str(e)}")
                    continue
            
            # 提交事务
            try:
                db.flush()
                db.commit()
                info(f"成功处理并存储作者笔记数据，作者ID: {auther_info.user_id}, 存储笔记数: {len(stored_notes)}")
                return stored_notes
            except Exception as e:
                db.rollback()
                error_detail = f"提交事务时出错: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
                error(error_detail)
                warning("由于事务提交错误，可能有部分数据未能成功存储")
                return []
                
        except Exception as e:
            db.rollback()
            error_detail = f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
            error(f"存储作者笔记过程中发生错误: {error_detail}")
            raise 

    @staticmethod
    def store_topics(db: Session, req_info: Dict[str, Any], topics_response: XhsTopicsResponse) -> List[XhsTopicDiscussion]:
        """存储话题数据，确保幂等性操作"""
        
        
        # 在开始前确保会话是干净的
        db.rollback()
        
        try:
            # 获取话题数据
            topics_data = topics_response.data.topic_list
            
            if not topics_data:
                warning("请求体中缺少有效的话题数据")
                return []
            
            info(f"开始处理话题数据，共 {len(topics_data)} 个话题")
            
            # 获取当前日期（只保留到日期部分）
            current_date = datetime.now().date()
            
            # 收集所有话题名称
            topic_names = [topic.name for topic in topics_data]
            
            # 查询当天已存在的话题记录
            existing_topics = {
                (topic.topic_name, topic.record_date): topic
                for topic in db.query(XhsTopicDiscussion).filter(
                    XhsTopicDiscussion.topic_name.in_(topic_names),
                    XhsTopicDiscussion.record_date == current_date
                ).all()
            }
            
            info(f"找到 {len(existing_topics)} 条当天已存在的话题记录")
            
            # 存储话题数据
            stored_topics = []
            
            for topic_item in topics_data:
                try:
                    # 转换浏览量为整数
                    view_num = int(topic_item.view_num) if topic_item.view_num.isdigit() else 0
                    
                    # 转换smart为布尔值
                    smart = topic_item.smart.lower() == "true"
                    
                    # 检查是否存在当天的记录
                    existing_topic = existing_topics.get((topic_item.name, current_date))
                    
                    if existing_topic:
                        # 更新现有记录
                        existing_topic.topic_type = topic_item.type
                        existing_topic.view_num = view_num
                        existing_topic.smart = smart
                        logger.debug(f"更新话题记录: {topic_item.name}")
                        stored_topics.append(existing_topic)
                    else:
                        # 创建新记录
                        new_topic = XhsTopicDiscussion(
                            topic_name=topic_item.name,
                            topic_type=topic_item.type,
                            view_num=view_num,
                            smart=smart,
                            record_date=current_date
                        )
                        db.add(new_topic)
                        stored_topics.append(new_topic)
                        logger.debug(f"创建新话题记录: {topic_item.name}")
                
                except Exception as e:
                    error(f"处理话题时出错 {topic_item.name}: {str(e)}")
                    continue
            
            # 提交事务
            try:
                db.flush()
                db.commit()
                info(f"成功处理并存储 {len(stored_topics)} 条话题数据")
                return stored_topics
            except Exception as e:
                db.rollback()
                error_detail = f"提交事务时出错: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
                error(error_detail)
                warning("由于事务提交错误，可能有部分数据未能成功存储")
                return []
                
        except Exception as e:
            db.rollback()
            error_detail = f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
            error(f"存储话题过程中发生错误: {error_detail}")
            raise