import os
import requests
import json
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Type, TypeVar, Generic, Callable

from app.config.settings import settings
from app.models.xhs_dao import XhsDAO
from app.models.xhs_models import XhsSearchResponse, XhsNote, XhsAutherNotesResponse, XhsComment, XhsCommentsResponse, XhsNoteDetail, XhsNoteDetailResponse, XhsTopicDiscussion, XhsTopicsResponse
from app.database.db import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.utils.logger import get_logger, info, warning, error, debug

# 获取当前模块的日志器
logger = get_logger(__name__)
# 定义泛型类型变量
T = TypeVar('T')

class XhsService:
    """小红书服务类，处理与小红书相关的业务逻辑"""
    
    @staticmethod
    def _call_coze_api(workflow_id: str, parameters: Dict[str, Any], mock_file_prefix: str) -> Dict[str, Any]:
        """
        调用Coze API并保存响应
        
        Args:
            workflow_id: 工作流ID
            parameters: API参数
            mock_file_prefix: mock文件前缀
            
        Returns:
            API响应结果
        """
        url = "https://api.coze.cn/v1/workflow/run"
        headers = {
            "Authorization": f"Bearer {settings.COZE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # 确保cookie存在于参数中
        if "cookie" not in parameters:
            parameters["cookie"] = settings.XHS_COOKIE
            
        payload = {
            "parameters": parameters,
            "workflow_id": workflow_id
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # 如果请求失败，抛出异常
            
            # 确保目录存在
            mock_dir = "mock/resp"
            date = datetime.now().strftime("%Y%m%d")
            os.makedirs(f"{mock_dir}/{mock_file_prefix}/{date}", exist_ok=True)
            # 生成文件名,使用时间戳避免重名
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{mock_dir}/{mock_file_prefix}/{date}/{timestamp}.json"
            # 保存响应内容
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
                
            return response.json()
            
        except Exception as e:
            error(f"调用Coze API失败: {e}")
            traceback.print_exc()
            return {}
    
    @staticmethod
    def _process_response(result: Dict[str, Any], response_type: Type[T]) -> Tuple[Optional[T], Dict[str, Any]]:
        """
        处理API响应并解析数据
        
        Args:
            result: API响应结果
            response_type: 响应对象类型
            
        Returns:
            解析后的响应对象和请求信息
        """
        if not result or not isinstance(result, dict) or "data" not in result:
            if result['code'] == 720702222:
                # We're currently experiencing server issues. Please try your request again after a short delay. If the problem persists, contact our support team.
                warning("Coze服务器正在维护，请稍后再试")
                return None, {}
            
            error("未找到data字段或result不是字典")
            info("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
            return None, {}
            
        if not isinstance(result["data"], str):
            error("data字段不是字符串")
            info("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
            return None, {}
            
        try:
            # 检查字符串是否为空
            if not result["data"]:
                error("data字段为空")
                return None, {}
                
            # 替换中文逗号为英文逗号
            data_json = json.loads(result["data"])
            
            # 检查resp_data字段
            if "resp_data" in data_json:
                resp_data = data_json["resp_data"]
                
                # 创建响应对象
                if response_type == XhsTopicsResponse:
                    response_obj = response_type(
                        code=data_json.get("resp_code", 0),
                        data=resp_data
                    )
                else:
                    response_obj = response_type(
                        status=data_json.get("resp_code", 0),
                        data=resp_data
                    )
                    
                return response_obj, data_json
            else:
                error("未找到resp_data字段,data字段内容:", json.dumps(data_json, ensure_ascii=False, indent=2))
                return None, {}
                
        except json.JSONDecodeError as e:
            error(f"data字段JSON解析错误: {e}")
            error("data字段内容:", result["data"])  # 打印原始字符串以便调试
            return None, {}
    
    @staticmethod
    def _store_data_in_db(db_method: Callable, req_info: Dict[str, Any], response_obj: Any, data_type: str = "笔记") -> List[Any]:
        """
        将数据存储到数据库
        
        Args:
            db_method: 数据库操作方法
            req_info: 请求信息
            response_obj: 响应对象
            data_type: 数据类型描述
            
        Returns:
            存储的数据列表
        """
        # 获取数据库会话
        db = next(get_db())
        stored_data = []
        
        try:
            # 确保数据库会话是干净的
            db.rollback()
            
            # 调用数据库操作方法
            stored_data = db_method(db, req_info, response_obj)
            info(f"成功存储 {len(stored_data) if isinstance(stored_data, list) else 1} 条{data_type}数据到数据库")
            
        except Exception as e:
            error(f"存储{data_type}数据到数据库时出错: {e}")
            traceback.print_exc()
            
        finally:
            db.close()
            
        return stored_data
    
    @staticmethod
    def get_notes_by_tag(tag: str = "", num: int = 10) -> List[XhsNote]:
        """
        根据标签获取小红书笔记
        
        Args:
            tag: 搜索的标签
            num: 获取的笔记数量
            
        Returns:
            存储的笔记列表
        """
        # 设置API参数
        parameters = {
            "search_tag": tag,
            "search_num": num,
            "cookie": settings.XHS_COOKIE
        }
        
        # 调用API
        result = XhsService._call_coze_api(
            workflow_id="7480441452158648331",
            parameters=parameters,
            mock_file_prefix="xhs_search"
        )
        
        # 处理响应
        response_obj, data_json = XhsService._process_response(result, XhsSearchResponse)
        if not response_obj:
            return []
            
        # 准备请求信息
        req_info = {
            "keywords": tag,
            "search_num": num
        }
        
        # 存储数据
        return XhsService._store_data_in_db(
            db_method=XhsDAO.store_search_results,
            req_info=req_info,
            response_obj=response_obj,
            data_type="笔记"
        )

    @staticmethod
    def get_notes_by_auther_id(auther_id: str) -> List[XhsNote]:
        """
        根据博主的用户Id获取全部笔记内容
        
        Args:
            auther_id: 博主的用户ID
            
        Returns:
            存储的笔记列表
        """
        user_profile_url = f"https://www.xiaohongshu.com/user/profile/{auther_id}"
        
        # 设置API参数
        parameters = {
            "userProfileUrl": user_profile_url,
            "cookie": settings.XHS_COOKIE
        }
        
        # 调用API
        result = XhsService._call_coze_api(
            workflow_id="7480852360857714739",
            parameters=parameters,
            mock_file_prefix="xhs_get_notes_by_auther"
        )
        
        # 处理响应
        response_obj, data_json = XhsService._process_response(result, XhsAutherNotesResponse)
        if not response_obj:
            return []
            
        # 准备请求信息
        req_info = {
            "userProfileUrl": user_profile_url
        }
        
        # 存储数据
        return XhsService._store_data_in_db(
            db_method=XhsDAO.store_auther_notes,
            req_info=req_info,
            response_obj=response_obj,
            data_type="笔记"
        )
    
    @staticmethod
    def get_comments_by_note_url(note_url: str, comments_num: int) -> List[XhsComment]:
        """
        根据笔记ID获取评论
        
        Args:
            note_id: 笔记ID
            xsec_token: 安全令牌
            comments_num: 评论数量
            
        Returns:
            存储的评论列表
        """
        
        # 设置API参数
        parameters = {
            "noteUrl": note_url,
            "comments_num": comments_num,
            "cookie": settings.XHS_COOKIE
        }
        
        # 调用API
        result = XhsService._call_coze_api(
            workflow_id="7480889721393152035",
            parameters=parameters,
            mock_file_prefix="xhs_get_comments_by_note"
        )
        
        # 处理响应
        response_obj, data_json = XhsService._process_response(result, XhsCommentsResponse)
        if not response_obj:
            return []
            
        # 准备请求信息
        req_info = {
            "noteUrl": note_url,
            "totalNumber": comments_num
        }
        
        # 存储数据
        return XhsService._store_data_in_db(
            db_method=XhsDAO.store_comments,
            req_info=req_info,
            response_obj=response_obj,
            data_type="评论"
        )
    
    @staticmethod
    def get_xhs_note_detail(note_url: str) -> List[XhsNoteDetail]:
        """
        获取笔记详情
        
        Args:
            note_id: 笔记ID
            xsec_token: 安全令牌
            
        Returns:
            存储的笔记详情
        """
        
        # 设置API参数
        parameters = {
            "noteUrl": note_url,
            "cookie": settings.XHS_COOKIE
        }
        
        # 调用API
        result = XhsService._call_coze_api(
            workflow_id="7480895021278920716",
            parameters=parameters,
            mock_file_prefix="xhs_get_note_detail"
        )
        
        # 处理响应
        response_obj, data_json = XhsService._process_response(result, XhsNoteDetailResponse)
        if not response_obj:
            return []
            
        # 准备请求信息
        req_info = {
            "noteUrl": note_url
        }
        
        # 存储数据
        return XhsService._store_data_in_db(
            db_method=XhsDAO.store_note_detail,
            req_info=req_info,
            response_obj=response_obj,
            data_type="笔记详情"
        )
    
    @staticmethod
    def get_topics(tag: str) -> List[XhsTopicDiscussion]:
        """
        获取话题列表
        
        Args:
            tag: 搜索的标签
            
        Returns:
            存储的话题列表
        """
        # 设置API参数
        parameters = {
            "keyword": tag,
            "cookie": settings.XHS_COOKIE
        }
        
        # 调用API
        result = XhsService._call_coze_api(
            workflow_id="7480898701533397031",
            parameters=parameters,
            mock_file_prefix="xhs_get_topics"
        )
        
        # 处理响应
        response_obj, data_json = XhsService._process_response(result, XhsTopicsResponse)
        if not response_obj:
            return []
            
        # 准备请求信息
        req_info = {
            "keyword": tag
        }
        
        # 存储数据
        return XhsService._store_data_in_db(
            db_method=XhsDAO.store_topics,
            req_info=req_info,
            response_obj=response_obj,
            data_type="话题"
        )
    
    @staticmethod
    def fix_note_tags():
        query = text("""
            select note_id, note_tags from xhs_note_details where note_tags != 'null'
                     """)
        db = next(get_db())
        result = db.execute(query)
        notes = [(row[0], row[1]) for row in result]
        if len(notes) == 0:
            info("没有需要处理的数据")
            return []
        
        for index, (note_id, note_tags) in enumerate(notes):
            info(f"处理第 {index} 条数据")
            try:
                decode_note_tags = json.loads(note_tags)
                new_note_tags_str = json.dumps(decode_note_tags, ensure_ascii=False)
                # 更新数据库中的记录
                update_query = text("""
                    UPDATE xhs_note_details 
                    SET note_tags = :new_note_tags 
                    WHERE note_id = :note_id
                """)
                db.execute(update_query, {"new_note_tags": new_note_tags_str, "note_id": note_id})
                
                # 提交更改
                db.commit()
            except Exception as e:
                error(f"出错: {note_id} - {e}")
                traceback.print_exc()
                
    @staticmethod
    def diagnose_note():
        query = text("""
            select n.note_id, n.note_display_title,
            d.note_desc, d.note_tags, d.comment_count, d.note_liked_count, d.share_count, d.collected_count
            from xhs_notes as n left join xhs_note_details as d
            on n.note_id = d.note_id where d.note_desc != '' and d.note_desc is not null 
            and d.note_create_time >= '2024-01-01'
            and n.note_id = '67ab7eb0000000002900bf33'
            """)
        db = next(get_db())
        result = db.execute(query)
        notes = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in result]
        if len(notes) == 0:
            info("没有需要处理的数据")
            return []
        
        for index, (note_id, note_display_title, note_desc, note_tags, comment_count, note_liked_count, share_count, collected_count) in enumerate(notes):
            info(f"处理第 {index} 条数据")
            # note_tags 处理一下，之前是 Unicode 编码，现在需要处理成中文
            # decode_note_tags = json.loads(note_tags)
            # note_tags = json.dumps(decode_note_tags, ensure_ascii=False)
            note_tags = json.loads(json.loads(note_tags))
            tags = "/".join(note_tags)
            try:
                note_content = f"""【标题】：{note_display_title}
【描述】：{note_desc}
【标签】：{tags}
【互动数据】：点赞 {note_liked_count} / 评论 {comment_count} / 分享 {share_count} / 收藏 {collected_count}"""
                # 获取LLM模型名称
                llm_name = "LLM模型名称"
                # 获取LLM模型版本
                model_version = "LLM模型版本"
                # todo 调用LLM模型进行诊断
                # 获取诊断结果
                diagnosis_result = "诊断结果"
                # 获取相关性得分
                relevance_score = 0.0
                # 存储诊断结果
                db.execute(text("""
                    INSERT INTO llm_note_diagnosis (note_id, llm_name, model_version, relevance_score, diagnosis_result)
                    VALUES (:note_id, :llm_name, :model_version, :relevance_score, :diagnosis_result)
                """), {
                    "note_id": note_id,
                    "llm_name": llm_name,
                    "model_version": model_version,
                    "relevance_score": relevance_score,
                    "diagnosis_result": diagnosis_result
                })
                db.commit()
            except Exception as e:  
                error(f"出错: {note_id} - {e}")
                traceback.print_exc()
            
                    