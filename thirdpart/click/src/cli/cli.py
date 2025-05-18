import os
import subprocess
import time
from typing import Iterator, Optional

import click

# 设置语言列表, 用于 type=click.Choice 类型的参数选项
LANGUAGE_SET = ["en", "zh"]


def _generate_output() -> Iterator[str]:
    """
    产生 100 行输出, 用于测试分页输出

    Yields:
        Generator[str, None, None]: 生成器, 输出每一条数据
    """
    for i in range(100):
        yield "Line {}\n".format(i)


def _get_commit_message() -> Optional[str]:
    """
    获取一条提交信息

    Returns:
        Union[List[str], None]: _description_
    """
    marker = "# Everything below is ignored\n"
    message = click.edit("\n\n" + marker)

    if message is None:
        return None

    return message.split(marker, 1)[0].rstrip("\n")


click_FILE_NAME = "click.txt"


@click.command("click")
@click.option("-n", "--name", "name",
              type=click.STRING, required=True,
              help="Name of people")
@click.option("-l", "--lang", "lang",
              type=click.Choice(LANGUAGE_SET), required=False,
              help="Language in {} and \"en\" is default".format(LANGUAGE_SET),
              default="en")
@click.option("-c", "--count", "count",
              type=click.IntRange(1, 20), required=False,
              help="Number between 1 and 20, default is 10",
              default=10)
@click.argument("color", type=click.STRING)
def cmd_click(name: str, lang: str, count: int, color: str) -> None:
    """
    click 命令, 演示 click 命令的基本使用

    通过一组 decorator 可以定义该命令的"选项"和"参数":

    - @click.option, 定义命令的选项, 包括:
        - 短名称, 长名称
        - 映射到的函数参数名
        - 参数类型 (type)
        - 是否必填 (required)
        - 帮助字符串 (help)
        - 默认值 (default)

    - @click.argument, 定义命令的参数，包括:
        - 参数名
        - 参数类型 (type)

    Args:
        name (str): --name 选项值
        lang (str): --lang 选项值
        count (int): --count 选项值
        color (str): color 参数值
    """
    # 清除屏幕
    click.clear()

    # click.echo 输出文本, click.style 用于为部分字符增加样式（前景色、背景色）
    click.echo(f"* name is \"{click.style(name, fg='red')}\"")
    click.echo(f"* language is \"{click.style(lang, bg='blue')}\"")
    click.echo(f"* count is \"{count}\"")
    click.echo(f"* color is: \"{click.style(color, fg=color)}\"")

    click.echo("Please input [Y]/n")
    # click.getchar 获取输入的字符
    c = (click.getchar().strip() or "y").lower()
    click.echo(f"Your input is: {click.style(c, fg='yellow')}")

    # 暂停，等待任意键输入
    click.pause()

    # 输出分页内容
    # 根据一个 iterator 或 generator 对象，进行分页输出
    click.echo_via_pager(_generate_output())

    # 获取一个提交信息, 该操作会打开预设的编辑器 (例如 gedit 或者 vim), 输入提交信息并保存
    _get_commit_message()
    click.echo(f"Your comment is: \"{_get_commit_message()}\"")

    # 启动编辑器, 编辑名为 click.txt 文件的内容
    click.edit(filename=click_FILE_NAME)

    # 输出上一步录入的内容
    if os.path.exists(click_FILE_NAME):
        output = subprocess.run(
            ["cat", click_FILE_NAME],
            check=True,
            capture_output=True,
        ).stdout.decode(encoding="utf-8")

        click.echo(f"File content of \"{click_FILE_NAME}\" file is: {output}")

    # 输出一个进度条
    max_ = [n for n in range(100)]
    with click.progressbar(max_, length=len(max_), label="Please waiting...") as bar:
        for n in bar:
            time.sleep(0.01)

    n = 50
    with click.progressbar(max_, length=100, label="Please waiting...") as bar:
        while n <= 100:
            time.sleep(1)
            # 更新进度条进度
            bar.update(n)
            n += n


@click.group()
def cli() -> None:
    """演示 click 框架命令行功能

    第一个 @click.group() 定义了根命令组, 所有的命令和子命令组需要加入到该命令组中
    """


# 将 click 命令添加到分组中
cli.add_command(cmd_click)


def main() -> None:
    cli()
