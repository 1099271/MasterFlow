import logging
import time
import sys

from typing import List
from sqlalchemy import text
from app.database.db import get_db
from app.services.xhs_service import XhsService

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
        logger = logging.getLogger(__name__)
        logger.info(f"开始搜索热门话题笔记，最小浏览量：{min_view_num}，话题限制：{topic_limit}")
        
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
                
            logger.info(f"找到 {len(topics)} 个符合条件的热门话题")
            
            if not topics:
                logger.error(f"没有找到符合条件的热门话题!")
                return 0

            # 遍历话题获取笔记
            total_notes = 0
            for topic in topics:
                # 确保键名存在
                topic_name = topic.get("topic_name", "未知话题")
                id = topic.get("id", topic.get("id", "未知ID"))
                view_num = topic.get("view_num", 0)
                
                if not topic_name or topic_name == "未知话题":
                    logger.warning(f"跳过无效话题: ID={id}")
                    continue
                
                logger.info(f"处理话题: {topic_name}(ID: {id})，浏览量: {view_num}")
                
                try:
                    # 使用话题名称作为标签获取笔记
                    notes = XhsService.get_notes_by_tag(topic_name, notes_per_topic)
                    total_notes += len(notes)
                    logger.info(f"成功获取话题 '{topic_name}' 的 {len(notes)} 条笔记")
                except Exception as e:
                    logger.error(f"获取话题 '{topic_name}' 的笔记时出错: {e}")
                    
                logger.info("等待60秒后处理下一个话题...")
                time.sleep(60)
            
            logger.info(f"任务完成，共处理 {len(topics)} 个话题，获取 {total_notes} 条笔记")
            return len(topics)
            
        except Exception as e:
            logger.error(f"查询热门话题时出错: {e}")
            import traceback
            traceback.print_exc()
            return 0
            
        finally:
            db.close()
