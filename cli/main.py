import typer
import sys
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
        mock_result = {'code': 0, 'cost': '0', 'data': '{"resp_code":0,"resp_data":[{"auther_avatar":"https://sns-avatar-qc.xhscdn.com/avatar/65aa73ea5e0a901295d5d39b.jpg?imageView2/2/w/80/format/jpg","auther_home_page_url":"https://www.xiaohongshu.com/user/profile/6565cfb7000000003c01d1a2","auther_nick_name":"野鲨","auther_user_id":"6565cfb7000000003c01d1a2","note_card_type":"normal","note_cover_height":"2388","note_cover_url_default":"http://sns-webpic-qc.xhscdn.com/202503121454/0c5733541aeb3b2726f20cd308409fb3/1040g2sg30ub2jb0jle005pb5purv3kd2tvt7hhg!nc_n_webp_mw_1","note_cover_url_pre":"http://sns-webpic-qc.xhscdn.com/202503121454/f4213b9a34bfe732ff53ec57b4544ba8/1040g2sg30ub2jb0jle005pb5purv3kd2tvt7hhg!nc_n_webp_prv_1","note_cover_width":"1668","note_display_title":"中国最后的母系氏族 没有婚姻制度非常幸福","note_id":"65b18c34000000000c0050f6","note_liked":false,"note_liked_count":"5383","note_model_type":"note","note_url":"https://www.xiaohongshu.com/explore/65b18c34000000000c0050f6?xsec_token=ABwI6y98bvx7dSMQKtWGyhC3oyAhsS_lHDBD19xD5e0iE=","note_xsec_token":"ABwI6y98bvx7dSMQKtWGyhC3oyAhsS_lHDBD19xD5e0iE="},{"auther_avatar":"https://sns-avatar-qc.xhscdn.com/avatar/62b41068732d149a6a1b8807.jpg?imageView2/2/w/80/format/jpg","auther_home_page_url":"https://www.xiaohongshu.com/user/profile/602e4957000000000101fc42","auther_nick_name":"Nnnmko","auther_user_id":"602e4957000000000101fc42","note_card_type":"normal","note_cover_height":"1920","note_cover_url_default":"http://sns-webpic-qc.xhscdn.com/202503121454/12d241eb9d42270deb8db2168a11d1fb/1000g00828sht8eifo0005o1e95bgbv22phsbvug!nc_n_webp_mw_1","note_cover_url_pre":"http://sns-webpic-qc.xhscdn.com/202503121454/f89108edfc6325563d9f647eb651e956/1000g00828sht8eifo0005o1e95bgbv22phsbvug!nc_n_webp_prv_1","note_cover_width":"1440","note_display_title":"纪录片｜中国唯一现存的母系社会「摩梭族」","note_id":"64244bab000000002702b7f4","note_liked":false,"note_liked_count":"16731","note_model_type":"note","note_url":"https://www.xiaohongshu.com/explore/64244bab000000002702b7f4?xsec_token=ABn5O1g0mc7dBkFQOeKnqS8Z6A55tIQcavQug07c42rqQ=","note_xsec_token":"ABn5O1g0mc7dBkFQOeKnqS8Z6A55tIQcavQug07c42rqQ="}，{"auther_avatar":"https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31btghbsj0k005okodhn8detrdt7qh9o?imageView2/2/w/80/format/jpg","auther_home_page_url":"https://www.xiaohongshu.com/user/profile/62986c6e000000002102bbbb","auther_nick_name":"石家庄市直综合岗小班开课中","auther_user_id":"62986c6e000000002102bbbb","note_card_type":"normal","note_cover_height":"571","note_cover_url_default":"http://sns-webpic-qc.xhscdn.com/202503121454/bb989abe7ebb9785de05235fdbe2c154/1040g2sg314vo8ps4h4405okodhn8detr466lhhg!nc_n_webp_mw_1","note_cover_url_pre":"http://sns-webpic-qc.xhscdn.com/202503121454/124c67f423902061d86400b17fe87213/1040g2sg314vo8ps4h4405okodhn8detr466lhhg!nc_n_webp_prv_1","note_cover_width":"629","note_display_title":"注意了！新华社公布新增57个禁用词","note_id":"668b843c0000000025009ed1","note_liked":false,"note_liked_count":"235","note_model_type":"note","note_url":"https://www.xiaohongshu.com/explore/668b843c0000000025009ed1?xsec_token=ABmuJZQZCJVOtVmFFwsEzRzoE7sYIYHr7gXXQol0J9xiA=","note_xsec_token":"ABmuJZQZCJVOtVmFFwsEzRzoE7sYIYHr7gXXQol0J9xiA="}]}', 'debug_url': 'https://www.coze.cn/work_flow?execute_id=7480812855509483531&space_id=7357987698298830857&workflow_id=7480441452158648331&execute_mode=2', 'msg': 'Success', 'token': 0}
        
        class MockResponse:
            def json(self):
                return mock_result
        
        # response = requests.post(url, headers=headers, json=payload)
        # response.raise_for_status()  # 如果请求失败，抛出异常
        
        response = MockResponse()
        result = response.json()
        
        # 检查result是否为字典
        if isinstance(result, dict) and "data" in result:
            if isinstance(result["data"], str):
                try:
                    # 检查字符串是否为空
                    if not result["data"]:
                        print("data字段为空")
                        return
                    
                    data_json = json.loads(result["data"])  # 尝试解析JSON
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
                    print("data字段内容:", result["data"])  # 打印原始字符串以便调试
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