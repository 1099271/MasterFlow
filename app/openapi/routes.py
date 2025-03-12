from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging
from datetime import datetime

from app.database.db import get_db
from app.models.xhs_models import SearchNoteRequest, XhsSearchResponse, XhsNoteItem, NoteDetailRequest, XhsNoteDetailResponse, CommentsRequest, XhsCommentsResponse, AutherNotesRequest, TopicsRequest
from app.models.xhs_dao import XhsDAO
from app.utils.response import ResponseBase, handle_error

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(tags=["OpenAPI"])

@router.post("/xhs_topics", response_model=Dict[str, Any], summary="小红书话题数据存储")
async def xhs_topics(
    request: TopicsRequest,
    db: Session = Depends(get_db)
):
    """
    存储小红书话题数据
    
    **参数**:
    - req_info: 请求信息，包含关键词等信息
    - req_body: 话题数据，包含话题列表
    
    **返回**:
    - 操作结果信息
    """
    # 确保数据库会话是干净的
    db.rollback()
    
    try:
        # 记录请求信息
        keyword = request.req_info.get('keyword', '')
        logger.info(f"接收到话题数据存储请求，关键词: {keyword}")
        
        # 验证请求体
        if not request.req_body or not request.req_body.data or not request.req_body.data.topic_list:
            logger.warning("请求体中缺少有效的话题数据")
            return ResponseBase.error(
                code=400,
                msg="未提供有效的话题数据"
            )
        
        # 存储话题数据
        try:
            stored_topics = XhsDAO.store_topics(db, request.req_info, request.req_body)
            
            if stored_topics:
                # 记录成功信息
                logger.info(f"成功存储话题数据，共 {len(stored_topics)} 个话题")
                
                # 返回结果
                return ResponseBase.success(
                    msg="话题数据存储成功",
                    data={
                        "stored_count": len(stored_topics),
                        "topic_names": [topic.topic_name for topic in stored_topics]
                    }
                )
            else:
                return ResponseBase.error(
                    code=500,
                    msg="存储话题数据失败"
                )
        except Exception as e:
            # 处理存储过程中的错误
            handle_error(e, "存储小红书话题数据")
            
            # 返回错误响应
            return ResponseBase.error(
                code=500,
                msg=f"执行存储小红书话题数据时发生错误: {str(e)}"
            )
        
    except Exception as e:
        # 统一错误处理
        handle_error(e, "处理小红书话题请求")
        
        # 返回统一的错误响应
        return ResponseBase.error(
            code=500,
            msg=f"处理小红书话题请求时发生错误: {str(e)}"
        )

@router.post("/xhs_search_note", response_model=Dict[str, Any], summary="小红书笔记搜索结果存储")
async def xhs_search_note(
    request: SearchNoteRequest,
    db: Session = Depends(get_db)
):
    """
    存储小红书笔记搜索结果
    
    **参数**:
    - req_info: 请求信息，包含搜索关键词等信息
    - req_body: 搜索结果数据，包含笔记列表
    
    **返回**:
    - 操作结果信息
    """
    # 确保数据库会话是干净的
    db.rollback()
    
    try:
        # 记录请求信息
        logger.info(f"接收到搜索结果存储请求，关键词: {request.req_info.get('keywords', '')}")
        
        # 验证请求体
        if not request.req_body or not request.req_body.data:
            logger.warning("请求体中缺少有效的搜索结果数据")
            return ResponseBase.error(
                code=400,
                msg="未提供有效的搜索结果数据"
            )
        
        # 验证数据类型
        try:
            # 检查关键字段的数据类型
            for note in request.req_body.data:
                # 确保数值字段可以被正确转换
                if note.note_cover_width and not str(note.note_cover_width).isdigit():
                    logger.warning(f"笔记 {note.note_id} 的封面宽度不是有效的数字: {note.note_cover_width}")
                    note.note_cover_width = None
                
                if note.note_cover_height and not str(note.note_cover_height).isdigit():
                    logger.warning(f"笔记 {note.note_id} 的封面高度不是有效的数字: {note.note_cover_height}")
                    note.note_cover_height = None
                
                if note.note_liked_count and not str(note.note_liked_count).isdigit():
                    logger.warning(f"笔记 {note.note_id} 的点赞数不是有效的数字: {note.note_liked_count}")
                    note.note_liked_count = "0"
        except Exception as e:
            logger.warning(f"数据类型验证过程中出现错误: {str(e)}")
            # 继续处理，让后续代码处理这些错误
        
        # 存储搜索结果
        try:
            stored_notes = XhsDAO.store_search_results(db, request.req_info, request.req_body)
            
            # 记录成功信息
            logger.info(f"成功存储 {len(stored_notes)} 条笔记数据")
            
            # 返回结果
            return ResponseBase.success(
                msg="数据存储成功",
                data={
                    "stored_count": len(stored_notes),
                    "note_ids": [note.note_id for note in stored_notes]
                }
            )
        except Exception as e:
            # 处理存储过程中的错误
            handle_error(e, "存储小红书笔记数据")
            
            # 返回错误响应
            return ResponseBase.error(
                code=500,
                msg=f"执行存储小红书笔记数据时发生错误: {str(e)}"
            )
        
    except Exception as e:
        # 统一错误处理
        handle_error(e, "处理小红书笔记搜索请求")
        
        # 返回统一的错误响应
        return ResponseBase.error(
            code=500,
            msg=f"处理小红书笔记搜索请求时发生错误: {str(e)}"
        )

@router.post("/xhs_note_detail", response_model=Dict[str, Any], summary="小红书笔记详情存储")
async def xhs_note_detail(
    request: NoteDetailRequest,
    db: Session = Depends(get_db)
):
    """
    存储小红书笔记详情
    
    **参数**:
    - req_info: 请求信息，包含笔记URL和关键词等信息
    - req_body: 笔记详情数据，包含笔记详细信息
    
    **返回**:
    - 操作结果信息
    """
    # 确保数据库会话是干净的
    db.rollback()
    
    try:
        # 记录请求信息
        note_url = request.req_info.get('noteUrl', '')
        logger.info(f"接收到笔记详情存储请求，笔记URL: {note_url}")
        
        # 验证请求体
        if not request.req_body or not request.req_body.data or not request.req_body.data.note or not request.req_body.data.note.note_id:
            logger.warning("请求体中缺少有效的笔记详情数据")
            return ResponseBase.error(
                code=400,
                msg="未提供有效的笔记详情数据"
            )
        
        # 存储笔记详情
        try:
            stored_note = XhsDAO.store_note_detail(db, request.req_info, request.req_body)
            
            if stored_note:
                # 记录成功信息
                logger.info(f"成功存储笔记详情数据，笔记ID: {stored_note.note_id}")
                
                # 返回结果
                return ResponseBase.success(
                    msg="笔记详情数据存储成功",
                    data={
                        "note_id": stored_note.note_id,
                        "note_url": stored_note.note_url,
                        "note_display_title": stored_note.note_display_title
                    }
                )
            else:
                return ResponseBase.error(
                    code=500,
                    msg="存储笔记详情数据失败"
                )
        except Exception as e:
            # 处理存储过程中的错误
            handle_error(e, "存储小红书笔记详情数据")
            
            # 返回错误响应
            return ResponseBase.error(
                code=500,
                msg=f"执行存储小红书笔记详情数据时发生错误: {str(e)}"
            )
        
    except Exception as e:
        # 统一错误处理
        handle_error(e, "处理小红书笔记详情请求")
        
        # 返回统一的错误响应
        return ResponseBase.error(
            code=500,
            msg=f"处理小红书笔记详情请求时发生错误: {str(e)}"
        )

@router.post("/xhs_comments", response_model=Dict[str, Any], summary="小红书评论数据存储")
async def xhs_comments(
    request: CommentsRequest,
    db: Session = Depends(get_db)
):
    """
    存储小红书评论数据
    
    **参数**:
    - req_info: 请求信息，包含笔记URL、关键词和总数等信息
    - req_body: 评论数据，包含评论列表
    
    **返回**:
    - 操作结果信息
    """
    # 确保数据库会话是干净的
    db.rollback()
    
    try:
        # 记录请求信息
        note_url = request.req_info.get('noteUrl', '')
        total_number = request.req_info.get('totalNumber', 0)
        logger.info(f"接收到评论数据存储请求，笔记URL: {note_url}, 总数: {total_number}")
        
        # 验证请求体
        if not request.req_body or not request.req_body.data or not request.req_body.data.comments:
            logger.warning("请求体中缺少有效的评论数据")
            return ResponseBase.error(
                code=400,
                msg="未提供有效的评论数据"
            )
        
        # 存储评论数据
        try:
            stored_comments = XhsDAO.store_comments(db, request.req_info, request.req_body)
            
            if stored_comments:
                # 记录成功信息
                logger.info(f"成功存储评论数据，共 {len(stored_comments)} 条评论")
                
                # 返回结果
                return ResponseBase.success(
                    msg="评论数据存储成功",
                    data={
                        "stored_count": len(stored_comments),
                        "comment_ids": [comment.comment_id for comment in stored_comments]
                    }
                )
            else:
                return ResponseBase.error(
                    code=500,
                    msg="存储评论数据失败"
                )
        except Exception as e:
            # 处理存储过程中的错误
            handle_error(e, "存储小红书评论数据")
            
            # 返回错误响应
            return ResponseBase.error(
                code=500,
                msg=f"执行存储小红书评论数据时发生错误: {str(e)}"
            )
        
    except Exception as e:
        # 统一错误处理
        handle_error(e, "处理小红书评论请求")
        
        # 返回统一的错误响应
        return ResponseBase.error(
            code=500,
            msg=f"处理小红书评论请求时发生错误: {str(e)}"
        )

@router.post("/xhs_auther_notes", response_model=Dict[str, Any], summary="小红书作者笔记数据存储")
async def xhs_auther_notes(
    request: AutherNotesRequest,
    db: Session = Depends(get_db)
):
    """
    存储小红书作者笔记数据
    
    **参数**:
    - req_info: 请求信息，包含作者主页URL和关键词等信息
    - req_body: 作者笔记数据，包含作者信息和笔记列表
    
    **返回**:
    - 操作结果信息
    """
    # 确保数据库会话是干净的
    db.rollback()
    
    try:
        # 记录请求信息
        user_profile_url = request.req_info.get('userProfileUrl', '')
        logger.info(f"接收到作者笔记数据存储请求，作者主页URL: {user_profile_url}")
        
        # 验证请求体
        if not request.req_body or not request.req_body.data or not request.req_body.data.auther_info:
            logger.warning("请求体中缺少有效的作者笔记数据")
            return ResponseBase.error(
                code=400,
                msg="未提供有效的作者笔记数据"
            )
        
        # 存储作者笔记数据
        try:
            stored_notes = XhsDAO.store_auther_notes(db, request.req_info, request.req_body)
            
            if stored_notes:
                # 记录成功信息
                logger.info(f"成功存储作者笔记数据，共 {len(stored_notes)} 条笔记")
                
                # 返回结果
                return ResponseBase.success(
                    msg="作者笔记数据存储成功",
                    data={
                        "stored_count": len(stored_notes),
                        "note_ids": [note.note_id for note in stored_notes],
                        "auther_id": request.req_body.data.auther_info.user_id
                    }
                )
            else:
                return ResponseBase.error(
                    code=500,
                    msg="存储作者笔记数据失败"
                )
        except Exception as e:
            # 处理存储过程中的错误
            handle_error(e, "存储小红书作者笔记数据")
            
            # 返回错误响应
            return ResponseBase.error(
                code=500,
                msg=f"执行存储小红书作者笔记数据时发生错误: {str(e)}"
            )
        
    except Exception as e:
        # 统一错误处理
        handle_error(e, "处理小红书作者笔记请求")
        
        # 返回统一的错误响应
        return ResponseBase.error(
            code=500,
            msg=f"处理小红书作者笔记请求时发生错误: {str(e)}"
        ) 