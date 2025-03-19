import typer
from app.services.xhs_service import XhsService
from app.services.topic_service import TopicService
from app.utils.logger import get_logger, info, warning, error, debug

# 获取当前模块的日志器
logger = get_logger(__name__)

app = typer.Typer()

@app.command(name="search_notes_by_topic")
def search_notes_by_topic(
    min_view_num: int = typer.Option(10000, "--min-view", "-v", help="最小话题浏览量"),
    topic_limit: int = typer.Option(20, "--topic-limit", "-l", help="处理话题的最大数量"),
    notes_per_topic: int = typer.Option(200, "--notes-per-topic", "-n", help="每个话题获取的笔记数量")
):
    """
    搜索热门话题的笔记
    
    从数据库中找到热门话题，然后获取这些话题的笔记并存储到数据库
    """
    info(f"开始搜索热门话题笔记，最小浏览量: {min_view_num}，处理话题数量上限: {topic_limit}")
    
    try:
        # 调用业务逻辑方法
        processed_topics = TopicService.search_notes_by_topic(
            min_view_num=min_view_num,
            topic_limit=topic_limit,
            notes_per_topic=notes_per_topic
        )
        
        if processed_topics > 0:
            info(f"任务完成! 共处理了 {processed_topics} 个话题")
        else:
            warning(f"没有找到符合条件的热门话题")
    except Exception as e:
        error(f"执行任务时出错: {e}")
        import traceback
        error(traceback.format_exc())

@app.command(name="deal_note_have_detail")
def deal_note_have_detail():
    """
    从数据库中查询没有详情页的笔记，然后获取详情页
    """
    
    try:
        # 调用业务逻辑方法
        processed_notes = TopicService.deal_note_have_detail()
        
        if processed_notes > 0:
            info(f"任务完成! 共处理了 {processed_notes} 个笔记")
        else:
            warning(f"没有找到符合条件的热门笔记")
    except Exception as e:
        error(f"执行任务时出错: {e}")
        import traceback
        error(traceback.format_exc())

@app.command(name="deal_note_comments")
def deal_note_comments():
    """
    从数据库中查询没有评论的笔记，然后获取评论
    """
    info(f"开始搜索没有评论的笔记")
    
    try:
        # 调用业务逻辑方法
        processed_notes = TopicService.deal_note_comments()
        
        if processed_notes > 0:
            info(f"任务完成! 共处理了 {processed_notes} 个笔记")
        else:
            warning(f"没有找到符合条件的热门笔记")
    except Exception as e:
        error(f"执行任务时出错: {e}")
        import traceback
        error(traceback.format_exc())
        
@app.command(name="fix_note_tags")
def fix_note_tags():
    try:
        XhsService.fix_note_tags()
    except Exception as e:
        error(f"执行任务时出错: {e}")
        import traceback
        error(traceback.format_exc())        

@app.command(name="export_note_content")
def export_note_content():
    try:
        XhsService.export_note_content()
    except Exception as e:
        error(f"执行任务时出错: {e}")
        import traceback
        error(traceback.format_exc())


if __name__ == "__main__":
    app()