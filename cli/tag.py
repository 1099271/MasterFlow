import typer
from app.utils.logger import get_logger, info, warning, error
from app.services.tag_service import TagService

# 获取当前模块的日志器
logger = get_logger(__name__)
app = typer.Typer()

@app.command(name="get_all_tags")
def get_all_tags():
    """
    获取所有标签
    """
    tags = TagService.get_tags_from_db()
    logger.info(f"获取到所有标签: {tags}")

@app.command(name="make_tags_from_note")
def make_tags_from_note(note_id: str = typer.Option(None, "--note_id", help="笔记ID")):
    """
    给指定的笔记提取标签
    """
    TagService.make_tags_from_note(note_id)

if __name__ == "__main__":
    app()