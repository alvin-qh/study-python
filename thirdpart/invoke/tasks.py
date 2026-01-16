from invoke.context import Context
from invoke.tasks import task

# Invoke 工具默认会在当前目录下寻找 `tasks.py` 文件并加载其中的任务
#
# `task.py` 文件可以包含多个任务函数, 每个函数都使用 `@task` 装饰器进行标记, 默认情况下, 函数名即为任务名, 通过
#
# ```bash
# invoke <task_name>
# ``
#
# 或
#
# ```bash
# inv <task_name>
# ```
#
# 命令行来运行指定任务
#
# 可使用 `inv[oke] --list` 或 `inv[oke] -l` 命令来列出所有可用任务


@task(
    name="lint",
    aliases=["fmt", "format"],
)
def lint(c: Context) -> None:
    """使用 `autopep8` 和 `pycln` 工具格式化和清理代码

    可以通过 `@task` 装饰器的参数来设定任务属性, 包括:

    - `name`: 任务名, 默认为函数名
    - `aliases`: 任务别名列表, 默认为空
    - `pre`: 任务前置任务列表, 默认为空
    - `post`: 任务后置任务列表, 默认为空
    - `default`: 是否为默认任务, 默认为 `False`
    - `optional`: 是否为可选任务, 默认为 `False`

    Args:
        `c` (`Context`): Invoke 任务上下文对象, 提供运行命令的方法
    """
    c.run("autopep8 .")
    c.run("pycln --config pyproject.toml")


@task
def type(c: Context) -> None:
    """使用 `mypy` 工具进行类型检查

    Args:
        `c` (`Context`): Invoke 任务上下文对象, 提供运行命令的方法
    """
    c.run("mypy")


@task
def test(c: Context) -> None:
    """使用 `pytest` 运行测试用例

    Args:
        `c` (`Context`): Invoke 任务上下文对象, 提供运行命令的方法
    """
    c.run("pytest")


@task(
    pre=[lint, type, test],
    default=True,
)
def check(c: Context) -> None:
    """组合任务, 运行 `lint`, `type` 和 `test` 任务

    Args:
        `c` (`Context`): Invoke 任务上下文对象, 提供运行命令的方法
    """
    pass
