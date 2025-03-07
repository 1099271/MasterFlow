from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.models.xhs_models import (
    XhsAuther, XhsNote, XhsKeywordGroup, XhsKeywordGroupNote, 
    XhsNoteItem, XhsSearchResponse, XhsNoteDetail
)
from datetime import datetime
import json
import logging
import traceback
import uuid
import sys

class XhsDAO:
    """小红书数据访问对象"""
    
    @staticmethod
    def get_or_create_auther(db: Session, auther_data: Dict[str, Any]) -> XhsAuther:
        """获取或创建作者记录"""
        auther_user_id = auther_data.get("auther_user_id")
        if not auther_user_id:
            print(f"警告：作者数据中缺少auther_user_id: {auther_data}")
            return None
        
        try:
            # 尝试查找作者
            auther = db.query(XhsAuther).filter(XhsAuther.auther_user_id == auther_user_id).first()
            
            # 如果作者不存在，创建新的作者记录
            if not auther:
                print(f"创建新作者: {auther_user_id}")
                auther = XhsAuther(
                    auther_user_id=auther_user_id,
                    auther_nick_name=auther_data.get("auther_nick_name"),
                    auther_avatar=auther_data.get("auther_avatar"),
                    auther_home_page_url=auther_data.get("auther_home_page_url")
                )
                db.add(auther)
                db.flush()
                print(f"新作者创建成功: {auther_user_id}")
            else:
                print(f"更新现有作者: {auther_user_id}")
                # 更新作者信息
                auther.auther_nick_name = auther_data.get("auther_nick_name", auther.auther_nick_name)
                auther.auther_avatar = auther_data.get("auther_avatar", auther.auther_avatar)
                auther.auther_home_page_url = auther_data.get("auther_home_page_url", auther.auther_home_page_url)
                auther.updated_at = datetime.now()
                print(f"作者信息更新成功: {auther_user_id}")
                
            return auther
            
        except Exception as e:
            print(f"处理作者数据时出错 {auther_user_id}: {str(e)}")
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
    def get_or_create_keyword_group(db: Session, keywords: List[str], group_name: Optional[str] = None) -> XhsKeywordGroup:
        """获取或创建关键词群组"""
        logger = logging.getLogger(__name__)
        
        # 确保keywords是字符串列表且不为空
        keywords = [str(k) for k in keywords if k]
        if not keywords:
            # 如果关键词为空，添加一个默认值避免空主键
            keywords = ["default"]
            logger.warning("关键词列表为空，使用默认关键词'default'")
        
        # 关键词列表为JSON字符串
        keywords_json = json.dumps(keywords, ensure_ascii=False)
        
        try:
            # 尝试查找关键词群组（精确匹配关键词列表）
            keyword_group = db.query(XhsKeywordGroup).filter(
                XhsKeywordGroup.keywords == keywords_json
            ).first()
            
            # 如果关键词群组不存在，创建新的关键词群组
            if not keyword_group:
                # 生成唯一的群组名称
                unique_group_name = group_name or f"关键词群组-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
                
                keyword_group = XhsKeywordGroup(
                    group_name=unique_group_name,
                    keywords=keywords_json  # 使用JSON字符串而不是原始列表
                )
                db.add(keyword_group)
                db.flush()
                logger.info(f"创建新的关键词群组: {unique_group_name}, 关键词: {keywords}")
            else:
                logger.info(f"找到现有关键词群组: {keyword_group.group_name}, ID: {keyword_group.group_id}")
                
            return keyword_group
            
        except Exception as e:
            logger.error(f"创建或获取关键词群组时出错: {str(e)}")
            # 创建一个临时的关键词群组对象，不保存到数据库
            # 这样即使出错，后续代码也能继续执行
            temp_group = XhsKeywordGroup(
                group_id=-1,  # 使用一个不可能的ID
                group_name="临时关键词群组",
                keywords=keywords_json
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
        logger = logging.getLogger(__name__)
        
        # 在开始前确保会话是干净的
        db.rollback()
        
        try:
            # 1. 首先收集所有需要处理的note_ids和auther_ids
            note_ids = [note.note_id for note in search_response.data]
            auther_ids = [note.auther_user_id for note in search_response.data]
            
            logger.info(f"开始处理 {len(note_ids)} 条笔记数据")
            
            # 2. 批量查询已存在的笔记和作者
            existing_notes = {}
            existing_authers = {}
            
            # 查询笔记
            try:
                existing_notes = {
                    note.note_id: note 
                    for note in db.query(XhsNote).filter(XhsNote.note_id.in_(note_ids)).all()
                }
                logger.info(f"找到 {len(existing_notes)} 条已存在的笔记")
            except Exception as e:
                logger.error(f"查询笔记信息时出错: {str(e)}")
            
            # 查询作者
            try:
                existing_authers = {
                    auther.auther_user_id: auther 
                    for auther in db.query(XhsAuther).filter(XhsAuther.auther_user_id.in_(auther_ids)).all()
                }
                logger.info(f"找到 {len(existing_authers)} 个已存在的作者")
            except Exception as e:
                logger.error(f"查询作者信息时出错: {str(e)}")
                
                # 尝试单独查询每个作者，以便找出问题所在
                for auther_id in auther_ids:
                    try:
                        auther = db.query(XhsAuther).filter(XhsAuther.auther_user_id == auther_id).first()
                        if auther:
                            existing_authers[auther.auther_user_id] = auther
                    except Exception as e2:
                        logger.error(f"查询单个作者 {auther_id} 时出错: {str(e2)}")
            
            # 3. 获取或创建关键词群组
            keyword_group = None
            existing_associations = set()
            
            keywords = [req_info.get("keywords")] if req_info.get("keywords") else []
            if keywords:
                # 确保关键词是字符串
                keywords = [str(k) for k in keywords if k]
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
                        logger.info(f"关键词群组: {keywords}, 已存在关联关系数量: {len(existing_associations)}")
                except Exception as e:
                    logger.error(f"处理关键词群组时出错: {str(e)}")
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
                        "note_image_list": None,
                        "note_tags": None,
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
                            logger.error(f"创建关键词关联时出错: {str(e)}")
                
                except Exception as e:
                    logger.error(f"处理笔记时出错 {getattr(note_item, 'note_id', '未知')}: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}")
                    continue
            
            # 5. 提交事务
            try:
                # 每100条记录提交一次，避免事务过大
                db.flush()
                db.commit()
                logger.info(f"成功处理并存储 {len(stored_notes)} 条笔记数据")
            except Exception as e:
                db.rollback()
                error_detail = f"提交事务时出错: {str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
                logger.error(error_detail)
                # 不抛出异常，而是返回已处理的笔记
                logger.warning("由于事务提交错误，可能有部分数据未能成功存储")
            
        except Exception as e:
            db.rollback()
            error_detail = f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
            logger.error(f"存储过程中发生错误: {error_detail}")
            raise
        
        return stored_notes 