import typer
from app.services.topic_service import TopicService

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
    print(f"开始搜索热门话题笔记，最小浏览量: {min_view_num}，处理话题数量上限: {topic_limit}")
    
    try:
        # 调用业务逻辑方法
        processed_topics = TopicService.search_notes_by_topic(
            min_view_num=min_view_num,
            topic_limit=topic_limit,
            notes_per_topic=notes_per_topic
        )
        
        if processed_topics > 0:
            print(f"任务完成! 共处理了 {processed_topics} 个话题")
        else:
            print(f"没有找到符合条件的热门话题")
    except Exception as e:
        print(f"执行任务时出错: {e}")
        import traceback
        traceback.print_exc()
    
if __name__ == "__main__":
    app()