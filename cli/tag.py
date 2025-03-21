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
    
@app.command(name="similar_tag")
def similar_tag(
    model_name: str = typer.Option("distiluse-v2", "--model", "-m", help="使用的预训练模型名称，可选值：'distiluse-v2', 'bge'")
):
    """
    给标签做相似度匹配
    
    Args:
        model_name: 使用的预训练模型名称，可选值：'distiluse-v2', 'bge'
    """
    tag_service = TagService(model_name=model_name)
    tag_service.similar_tag()
    
@app.command(name="analyse_tag_similarity")
def analyse_tag_similarity(
    note_id: str = typer.Option(None, "--note_id", help="笔记ID"),
    model_name: str = typer.Option("distiluse-v2", "--model", "-m", help="使用的预训练模型名称，可选值：'distiluse-v2', 'bge'")
):
    """
    分析标签相似度
    
    Args:
        note_id: 笔记ID，可选
        model_name: 使用的预训练模型名称，可选值：'distiluse-v2', 'bge'
    """
    # 创建 TagService 实例
    tag_service = TagService(model_name=model_name)
    
    # 初始化标准标签
    # tag_service.init_standard_tags()
    
    # 分析标签相似度
    tag_service.analyse_tag_similarity(note_id)

if __name__ == "__main__":
    app()