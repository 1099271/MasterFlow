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
    tag: str = typer.Option("摩梭族", "--tag", "-t", help="搜索的标签"),
    num: int = typer.Option(10, "--num", "-n", help="获取的笔记数量")
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


if __name__ == "__main__":
    app()