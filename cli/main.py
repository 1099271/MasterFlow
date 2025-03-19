import typer
from cli.xhs import app as xhs_app
from cli.tag import app as tag_app
from cli.spider import app as spider_app
from app.utils.logger import get_logger, info

# 获取当前模块的日志器
logger = get_logger(__name__)
app = typer.Typer()

# 添加子应用
app.add_typer(xhs_app, name="xhs")
app.add_typer(tag_app, name="tag")
app.add_typer(spider_app, name="spider")

if __name__ == "__main__":
    app()