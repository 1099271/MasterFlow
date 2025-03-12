import typer
from app.services.topic_service import TopicService

app = typer.Typer()

@app.command(name="search_notes_by_topic")
def search_notes_by_topic():
    """
    搜索笔记
    """
    TopicService.search_notes_by_topic()
    
if __name__ == "__main__":
    app()