from toolchain_setup.service import load_users

import click

# 读取所有用户信息
USERS = load_users()


@click.command("login")
@click.option(
    "-i",
    "--id",
    "id_",
    type=click.STRING,
    required=True,
    prompt=True,
    help="User ID",
)
@click.option(
    "-n",
    "--name",
    "name_",
    type=click.STRING,
    required=True,
    prompt=True,
    help="User name",
)
def login(id_: str, name_: str) -> None:
    """登录命令

    Args:
        id (str): 用户 ID
        name (str): 用户名称
    """
    user = next(filter(lambda user: user.id == id_, USERS), None)
    if user is None:
        print("User not found")
        exit(1)

    if name_ != user.name:
        print("User name does not match")
        exit(1)

    user_password = input("Enter user password: ")
    if user_password != user.password:
        print("User password does not match")
        exit(1)

    print(f"Login successful, Hello {user.name}")


@click.group()
def cli() -> None:
    """命令行"""


# 为命令行分组添加命令行函数
cli.add_command(login)
