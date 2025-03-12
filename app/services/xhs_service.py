import os
import requests
import json
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.config.settings import settings
from app.models.xhs_dao import XhsDAO
from app.models.xhs_models import XhsSearchResponse, XhsNote, XhsAutherNotesResponse
from app.database.db import get_db
from sqlalchemy.orm import Session


class XhsService:
    """小红书服务类，处理与小红书相关的业务逻辑"""
    
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
        url = "https://api.coze.cn/v1/workflow/run"
        
        headers = {
            "Authorization": f"Bearer {settings.COZE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "parameters": {
                "search_tag": tag,
                "search_num": num,
                "cookie": settings.XHS_COOKIE
            },
            "workflow_id": "7480441452158648331"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # 如果请求失败，抛出异常

            # 确保目录存在
            mock_dir = "mock/resp"
            os.makedirs(mock_dir, exist_ok=True)

            # 生成文件名,使用时间戳避免重名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{mock_dir}/xhs_search_{timestamp}.json"

            # 保存响应内容
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
                
            result = response.json()
            stored_notes = []

            # 检查result是否为字典
            if isinstance(result, dict) and "data" in result:
                if isinstance(result["data"], str):
                    try:
                        # 检查字符串是否为空
                        if not result["data"]:
                            print("data字段为空")
                            return []
                        
                        # 替换中文逗号为英文逗号
                        data_json = json.loads(result["data"].replace('，', ','))
                        
                        # 检查resp_data字段
                        if "resp_data" in data_json:
                            resp_data = data_json["resp_data"]
                            
                            # 将resp_data转换为XhsSearchResponse对象并存储到数据库
                            search_response = XhsSearchResponse(
                                status=data_json.get("resp_code", 0),  # 使用外层的resp_code
                                data=resp_data  # resp_data本身就是列表
                            )
                            
                            # 准备请求信息
                            req_info = {
                                "keywords": tag,
                                "search_num": num
                            }
                            
                            # 获取数据库会话
                            db = next(get_db())
                            try:
                                # 确保数据库会话是干净的
                                db.rollback()
                                
                                # 调用XhsDAO.store_search_results方法存储搜索结果
                                stored_notes = XhsDAO.store_search_results(db, req_info, search_response)
                                print(f"成功存储 {len(stored_notes)} 条笔记数据到数据库")
                            except Exception as e:
                                print(f"存储笔记数据到数据库时出错: {e}")
                                traceback.print_exc()
                            finally:
                                db.close()
                        else:
                            print("未找到resp_data字段,data字段内容:", json.dumps(data_json, ensure_ascii=False, indent=2))
                    except json.JSONDecodeError as e:
                        print(f"data字段JSON解析错误: {e}")
                        print("data字段内容:", result["data"])  # 打印原始字符串以便调试
                else:
                    print("未找到data字段或result不是字典")
                    print("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("未找到data字段或result不是字典")
                print("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
                
            return stored_notes
        
        except Exception as e:
            print(f"获取小红书笔记失败: {e}")
            traceback.print_exc()
            return []

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

        url = "https://api.coze.cn/v1/workflow/run"
        headers = {
            "Authorization": f"Bearer {settings.COZE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "parameters": {
                "user_profile_url": user_profile_url,
                "cookie": settings.XHS_COOKIE
            },
            "workflow_id": "7480852360857714739"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 如果请求失败，抛出异常
        
        # 确保目录存在
        mock_dir = "mock/resp"
        os.makedirs(mock_dir, exist_ok=True)

        # 生成文件名,使用时间戳避免重名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{mock_dir}/xhs_get_notes_by_auther_{timestamp}.json"

        # 保存响应内容
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
        
        result = response.json()
        if isinstance(result, dict) and "data" in result:
                if isinstance(result["data"], str):
                    try:
                        # 检查字符串是否为空
                        if not result["data"]:
                            print("data字段为空")
                            return []

                        # 替换中文逗号为英文逗号
                        data_json = json.loads(result["data"].replace('，', ','))
                        
                        # 检查resp_data字段
                        if "resp_data" in data_json:
                            resp_data = data_json["resp_data"]
                            
                            # 将resp_data转换为XhsSearchResponse对象并存储到数据库
                            search_response = XhsAutherNotesResponse(
                                status=data_json.get("resp_code", 0),  # 使用外层的resp_code
                                data=resp_data  # resp_data本身就是列表
                            )
                            
                            # 准备请求信息
                            req_info = {
                                "userProfileUrl": user_profile_url
                            }
                            
                            # 获取数据库会话
                            db = next(get_db())
                            try:
                                # 确保数据库会话是干净的
                                db.rollback()
                                
                                # 调用XhsDAO.store_auther_notes方法存储搜索结果
                                stored_notes = XhsDAO.store_auther_notes(db, req_info, search_response)
                                print(f"成功存储 {len(stored_notes)} 条笔记数据到数据库")
                            except Exception as e:
                                print(f"存储笔记数据到数据库时出错: {e}")
                                traceback.print_exc()
                            finally:
                                db.close()
                        else:
                            print("未找到resp_data字段,data字段内容:", json.dumps(data_json, ensure_ascii=False, indent=2))
                    except json.JSONDecodeError as e:
                        print(f"data字段JSON解析错误: {e}")
                        print("data字段内容:", result["data"])  # 打印原始字符串以便调试
                else:
                    print("未找到data字段或result不是字典")
                    print("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("未找到data字段或result不是字典")
            print("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
            
        return stored_notes