import typer
import os
import requests
import json
from app.config.settings import settings
from app.models.xhs_dao import XhsDAO
from sqlalchemy.orm import Session
from app.models.xhs_models import XhsSearchResponse
from app.database.db import get_db

app = typer.Typer()

@app.command()
def main(
    tag: str = typer.Option("摩梭族", "--tag", "-t", help="搜索的标签"),
    num: int = typer.Option(10, "--num", "-n", help="获取的笔记数量")
):
    """
    获取小红书笔记的命令行工具
    """
    # 获取小红书笔记
    get_xhs_notes_by_Tag(tag, num)
    
    
def get_xhs_notes_by_Tag(tag="摩梭族", num=10):
    """
    根据标签获取小红书笔记
    
    Args:
        tag: 搜索的标签
        num: 获取的笔记数量
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
        
        # 解析JSON响应
        result = response.json()
        
        # 检查result是否为字典
        if isinstance(result, dict) and "data" in result:
            if isinstance(result["data"], str):
                try:
                    data_json = json.loads(result["data"])
                    # 检查resp_data字段
                    if "resp_data" in data_json:
                        resp_data = data_json["resp_data"]
                        print(json.dumps(resp_data, ensure_ascii=False, indent=2))
                        
                        # 将resp_data转换为XhsSearchResponse对象并存储到数据库
                        search_response = XhsSearchResponse(
                            status=resp_data.get("status", 0),
                            data=resp_data.get("data", [])
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
                            import traceback
                            traceback.print_exc()
                        finally:
                            db.close()
                    else:
                        print("未找到resp_data字段,data字段内容:", json.dumps(data_json, ensure_ascii=False, indent=2))
                except json.JSONDecodeError as e:
                    print(f"data字段JSON解析错误: {e}")
                    print("data字段内容:", result["data"])
            else:
                print("未找到data字段或result不是字典")
                print("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("未找到data字段或result不是字典")
            print("返回的完整数据:", json.dumps(result, ensure_ascii=False, indent=2))
    
    except Exception as e:
        print(f"获取小红书笔记失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    app()