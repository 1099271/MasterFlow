import typer
from app.services.xhs_service import XhsService

app = typer.Typer()

@app.command(name="")
def main():
    """
    默认命令，显示欢迎信息
    """
    print("欢迎使用小红书爬虫工具")
    print("使用 --help 查看所有可用命令")

@app.command(name="get_notes_by_tag")
def get_xhs_notes_by_tag_cli(
    tag: str = typer.Option(..., "--tag", "-t", help="搜索的标签"),
    num: int = typer.Option(..., "--num", "-n", help="获取的笔记数量")
):
    """
    根据标签获取小红书笔记
    """
    print(f"正在获取标签 '{tag}' 的 {num} 条笔记...")
    notes = XhsService.get_notes_by_tag(tag, num)
    print(f"完成! 共获取了 {len(notes)} 条笔记")

@app.command(name="get_notes_by_auther")
def get_xhs_notes_by_auther_id_cli(
    auther_id: str = typer.Option(..., "--auther_id", "-a", help="博主的用户ID")
):
    """
    根据博主的用户ID获取全部笔记内容
    """
    print(f"正在获取博主 '{auther_id}' 的所有笔记...")
    notes = XhsService.get_notes_by_auther_id(auther_id)
    print(f"完成! 共获取了 {len(notes)} 条笔记")

@app.command(name="get_comments_by_note")
def get_xhs_comments_by_note_id_cli(
    note_id: str = typer.Option(..., "--note_id", "-nid", help="笔记的链接Id"),
    xsec_token: str = typer.Option(..., "--xsec_token", "-x", help="笔记的xsec_token"),
    comments_num: int = typer.Option(100, "--num", "-n", help="评论数量")
):
    """
    根据笔记Id获取评论信息
    """
    print(f"正在获取该帖子下的全部评论")
    comments = XhsService.get_comments_by_note_id(note_id, xsec_token, comments_num)
    print(f"Done!一共获取到了 {len(comments)} 条评论")

@app.command(name="get_note_detail")
def get_xhs_note_detail_cli(
    note_id: str = typer.Option(..., "--note_id", "-nid", help="笔记的链接Id"),
    xsec_token: str = typer.Option(..., "--xsec_token", "-x", help="笔记的xsec_token")
):
    """
    获取某个笔记的详情数据
    """
    print(f"正在获取该笔记详细信息")
    XhsService.get_xhs_note_detail(note_id, xsec_token)
    print(f"Done!")
    
@app.command(name="get_topics")
def get_xhs_topics_cli(
    tag: str = typer.Option(..., "--tag", "-t", help="搜索的标签")
):
    """
    获取某个笔记的详情数据
    """
    print(f"正在获取该话题详细信息")
    res_topics = XhsService.get_topics(tag)
    print(f"Done! 共获取到了 {len(res_topics)} 个话题")

if __name__ == "__main__":
    app()