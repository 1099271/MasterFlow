import typer
from app.services.xhs_service import XhsService
from cli.xhs import app as xhs_app
from app.utils.logger import get_logger, info, warning, error, debug

# 获取当前模块的日志器
logger = get_logger(__name__)
app = typer.Typer()

@app.command(name="")
def main():
    """
    默认命令，显示欢迎信息
    """
    info("使用 --help 查看所有可用命令")

@app.command(name="get_notes_by_tag")
def get_xhs_notes_by_tag_cli(
    tag: str = typer.Option(..., "--tag", "-t", help="搜索的标签"),
    num: int = typer.Option(..., "--num", "-n", help="获取的笔记数量")
):
    """
    根据标签获取小红书笔记
    """
    info(f"正在获取标签 '{tag}' 的 {num} 条笔记...")
    notes = XhsService.get_notes_by_tag(tag, num)
    info(f"完成! 共获取了 {len(notes)} 条笔记")

@app.command(name="get_notes_by_auther")
def get_xhs_notes_by_auther_id_cli(
    auther_id: str = typer.Option(..., "--auther_id", "-a", help="博主的用户ID")
):
    """
    根据博主的用户ID获取全部笔记内容
    """
    info(f"正在获取博主 '{auther_id}' 的所有笔记...")
    notes = XhsService.get_notes_by_auther_id(auther_id)
    info(f"完成! 共获取了 {len(notes)} 条笔记")

@app.command(name="get_comments_by_note")
def get_xhs_comments_by_note_id_cli(
    note_url: str = typer.Option(..., "--note_url", "-url", help="笔记的链接"),
    comments_num: int = typer.Option(100, "--num", "-n", help="评论数量")
):
    """
    根据笔记Id获取评论信息
    """
    info(f"正在获取该帖子下的全部评论")
    comments = XhsService.get_comments_by_note_id(note_url, comments_num)
    info(f"Done!一共获取到了 {len(comments)} 条评论")

@app.command(name="get_note_detail")
def get_xhs_note_detail_cli(
    note_url: str = typer.Option(..., "--note_url", "-url", help="笔记的链接")
):
    """
    获取某个笔记的详情数据
    """
    info(f"正在获取该笔记详细信息")
    XhsService.get_xhs_note_detail(note_url)
    info(f"Done!")
    
@app.command(name="get_topics")
def get_xhs_topics_cli(
    tag: str = typer.Option(..., "--tag", "-t", help="搜索的标签")
):
    """
    获取某个笔记的详情数据
    """
    info(f"正在获取该话题详细信息")
    res_topics = XhsService.get_topics(tag)
    info(f"Done! 共获取到了 {len(res_topics)} 个话题")

if __name__ == "__main__":
    app()