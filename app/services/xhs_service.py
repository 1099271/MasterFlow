import os
import time
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
from app.utils.logger import get_logger, info, warning, error, debug
from rich import print as rich_print

# 获取当前模块的日志器
logger = get_logger(__name__)
# 定义泛型类型变量
T = TypeVar('T')

class XhsService:
    """小红书服务类，处理与小红书相关的业务逻辑"""
    max_retries = 5
    
    @staticmethod
    def _call_coze_api(workflow_id: str, parameters: Dict[str, Any], log_file_prefix: str, retries: int = 0) -> Dict[str, Any]:
        """
        调用Coze API并保存响应
        
        Args:
            workflow_id: 工作流ID
            parameters: API参数
            log_file_prefix: log文件前缀
            
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
            log_dir = "logs/coze_http_request"
            date = datetime.now().strftime("%Y%m%d")
            os.makedirs(f"{log_dir}/{log_file_prefix}/{date}", exist_ok=True)
            # 生成文件名,使用时间戳避免重名
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{log_dir}/{log_file_prefix}/{date}/{timestamp}.json"
            # 保存响应内容
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
            
            resp_json = response.json()
            # 根据响应状态码处理逻辑
            match resp_json.get("code"):
                case 4013:
                    # 请求频率超出限制，等待60秒后重试
                    time.sleep(60)
                    return XhsService._call_coze_api(workflow_id, parameters, log_file_prefix, retries + 1)
                case 720702222:
                    # We're currently experiencing server issues. Please try your request again after a short delay. If the problem persists, contact our support team.
                    time.sleep(120)
                    return XhsService._call_coze_api(workflow_id, parameters, log_file_prefix, retries + 1)
                case _:
                    if resp_json.get("code") != 0:
                        error(f"请求Coze出现异常:{resp_json.get('code')}|{resp_json.get('msg')}")
                    return resp_json
                
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
            log_file_prefix="get_notes_by_tag"
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
            log_file_prefix="xhs_get_notes_by_auther"
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
            log_file_prefix="xhs_get_comments_by_note"
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
            log_file_prefix="xhs_get_note_detail"
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
            log_file_prefix="xhs_get_topics"
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
    def export_note_content():
        query = text("""
            select n.note_id, n.note_display_title,
            d.note_desc, d.note_tags, d.comment_count, d.note_liked_count, d.share_count, d.collected_count
            from xhs_notes as n left join xhs_note_details as d
            on n.note_id = d.note_id where d.note_desc != '' and d.note_desc is not null 
            and d.note_create_time >= '2024-01-01'
            and d.note_tags is not null
            limit 100
            """)
        db = next(get_db())
        result = db.execute(query)
        notes = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in result]
        if len(notes) == 0:
            info("没有需要处理的数据")
            return []
        
        for index, (note_id, note_display_title, note_desc, note_tags, comment_count, note_liked_count, share_count, collected_count) in enumerate(notes):
            info(f"处理第 {index} 条数据")
            try:
                note_tags = XhsService.process_note_tags(note_tags)
                tags = "/".join(note_tags)
                note_content = f"""
【标题】：{note_display_title}
【描述】：{note_desc}
【标签】：{tags}
【互动数据】：点赞 {note_liked_count} / 评论 {comment_count} / 分享 {share_count} / 收藏 {collected_count}"""
                # 确保目录存在
                log_dir = "logs/note_content"
                date = datetime.now().strftime("%Y%m%d")
                os.makedirs(f"{log_dir}/{date}", exist_ok=True)
                
                filename = f"{log_dir}/{date}/normal_level_note_content.txt"
                
                # 保存笔记内容
                # 追加写入笔记内容
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(note_content + "\n<|next_post|>\n")
                    
                info(f"笔记内容已保存到: {filename}")
            except Exception as e:  
                error(f"出错: {note_id} - {e}")
                traceback.print_exc()
    
    @staticmethod
    def process_note_tags(note_tags):
        try:
            
            # 情况 1：如果已经是列表，直接返回
            if isinstance(note_tags, list):
                return note_tags
            
            # 情况 2：尝试第一次解析
            try:
                note_tags = json.loads(note_tags)
            except json.JSONDecodeError:
                # 如果解析失败，说明 note_tags 不是有效的 JSON 字符串
                raise ValueError("note_tags 不是有效的 JSON 字符串")
            
            # 情况 3：检查是否需要第二次解析
            if isinstance(note_tags, str):
                # 如果解析后仍然是字符串，尝试再次解析
                note_tags = json.loads(note_tags)
            
            # 确保最终结果是列表
            if not isinstance(note_tags, list):
                raise ValueError("解析后的 note_tags 不是列表")
            
            return note_tags
        
        except Exception as e:
            error(f"处理 note_tags 出错: {e}")
            raise
        
                    