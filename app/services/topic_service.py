import time
import sys
import random
from typing import List
from sqlalchemy import text
from app.database.db import get_db
from app.services.xhs_service import XhsService
from app.utils.logger import get_logger, info, warning, error, debug
import traceback

# 获取当前模块的日志器
logger = get_logger(__name__)

class TopicService:
    @staticmethod
    def search_notes_by_topic(min_view_num: int = 10000, topic_limit: int = 20, notes_per_topic: int = 200):
        """
        根据热门话题搜索笔记
        
        从xhs_topic_discussions表中找到符合条件的热门话题，然后根据这些话题获取笔记
        
        Args:
            min_view_num: 最小浏览量，默认10000
            topic_limit: 处理话题的最大数量，默认20个
            notes_per_topic: 每个话题获取的笔记数量，默认200
            
        Returns:
            处理的话题数量
        """
        info(f"开始搜索热门话题笔记，最小浏览量：{min_view_num}，话题限制：{topic_limit}")
        
        # 获取数据库连接
        db = next(get_db())
        try:
            # 查询满足条件的热门话题
            query = text("""
                SELECT id, id, topic_name, view_num
                FROM xhs_topic_discussions
                WHERE view_num > :min_view_num
                ORDER BY view_num DESC
                LIMIT :limit
            """)
            
            result = db.execute(
                query, 
                {"min_view_num": min_view_num, "limit": topic_limit}
            )
            
            # 正确处理查询结果 - 使用SQLAlchemy的行映射
            topics = []
            for row in result:
                # 使用行的键值对方式访问(可能需要根据实际数据库字段调整)
                topic = {
                    "id": row[0],                    # id
                    "id": row[1] if len(row) > 1 else row[0],  # id 如果存在，否则使用id
                    "topic_name": row[2] if len(row) > 2 else None,  # topic_name
                    "view_num": row[3] if len(row) > 3 else 0       # view_num
                }
                topics.append(topic)
                
            info(f"找到 {len(topics)} 个符合条件的热门话题")
            
            if not topics:
                error(f"没有找到符合条件的热门话题!")
                return 0

            # 遍历话题获取笔记
            total_notes = 0
            for topic in topics:
                # 确保键名存在
                topic_name = topic.get("topic_name", "未知话题")
                id = topic.get("id", topic.get("id", "未知ID"))
                view_num = topic.get("view_num", 0)
                
                if not topic_name or topic_name == "未知话题":
                    warning(f"跳过无效话题: ID={id}")
                    continue
                
                info(f"处理话题: {topic_name}(ID: {id})，浏览量: {view_num}")
                
                try:
                    # 使用话题名称作为标签获取笔记
                    notes = XhsService.get_notes_by_tag(topic_name, notes_per_topic)
                    total_notes += len(notes)
                    info(f"成功获取话题 '{topic_name}' 的 {len(notes)} 条笔记")
                except Exception as e:
                    error(f"获取话题 '{topic_name}' 的笔记时出错: {e}")
    
                    error(traceback.format_exc())
                    
                info("等待60秒后处理下一个话题...")
                time.sleep(60)
            
            info(f"任务完成，共处理 {len(topics)} 个话题，获取 {total_notes} 条笔记")
            return len(topics)
            
        except Exception as e:
            error(f"查询热门话题时出错: {e}")
            error(traceback.format_exc())
            return 0
            
        finally:
            db.close()

    @staticmethod
    def deal_note_have_detail():
        """
        处理没有详情页的笔记
        """
        info(f"开始处理没有详情页的笔记")

        # 获取数据库连接
        db = next(get_db())
        processed_count = 0
        
        try:
            # 查询没有详情页的笔记
            query = text("""
                SELECT xhs_notes.note_url
                FROM xhs_notes left join xhs_note_details on xhs_notes.note_id = xhs_note_details.note_id
                WHERE xhs_note_details.note_desc is null or xhs_note_details.note_id is null
            """)

            result = db.execute(query)
            note_urls = [row[0] for row in result]
            
            info(f"------------ 找到 {len(note_urls)} 条没有详情页的笔记 ----------------")
            
            for index, note_url in enumerate(note_urls):
                info(f"处理第 {index} 条笔记: {note_url}")
                # 获取详情页
                try:
                    detail = XhsService.get_xhs_note_detail(note_url)
                    if detail:
                        processed_count += 1
                    else:
                        warning(f"获取笔记详情页失败: {note_url}")
                except Exception as e:
                    error(f"获取笔记详情页出错: {note_url} - {e}")
                    
                # 随机等待1-5秒
                sleep_time = random.randint(1, 5)
                debug(f"等待 {sleep_time} 秒后继续...")
                time.sleep(sleep_time)
                
            info(f"任务完成，共处理 {processed_count} 条笔记")
            return processed_count
            
        except Exception as e:
            error(f"处理笔记详情时出错: {e}")
            error(traceback.format_exc())
            return 0
            
        finally:
            db.close()
    
    @staticmethod
    def deal_note_comments():
        """
        处理没有评论的笔记
        """
        info(f"开始处理没有评论的笔记")

        # 获取数据库连接
        db = next(get_db())
        processed_count = 0
        
        try:
            # 查询没有详情页的笔记
            query = text("""
                select note_url, comment_count, note_liked_count
                from xhs_note_details where comment_count > 0 and note_liked_count > 0
            """)

            result = db.execute(query)
            note_data = [(row[0], row[1]) for row in result]
            
            info(f"找到 {len(note_data)} 条需要获取评论的笔记")
            
            for note_url, comment_count in note_data:
                info(f"处理笔记: {note_url}, 评论数: {comment_count}")
                # 获取评论
                try:
                    comments = XhsService.get_comments_by_note_url(note_url, comment_count)
                    if comments:
                        info(f"获取笔记评论成功: {note_url} - {len(comments)} 条评论")
                        processed_count += 1
                    else:
                        warning(f"获取笔记评论失败: {note_url}")
                except Exception as e:
                    error(f"获取笔记评论出错: {note_url} - {e}")
                
                # 随机等待60-100秒，避免频繁请求
                sleep_time = random.randint(60, 100)
                info(f"等待 {sleep_time} 秒后继续...")
                time.sleep(sleep_time)
                
            info(f"任务完成，共处理 {processed_count} 条笔记评论")
            return processed_count
            
        except Exception as e:
            error(f"处理笔记评论时出错: {e}")
            error(traceback.format_exc())
            return 0
            
        finally:
            db.close()