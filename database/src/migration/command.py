import os

from alembic import command, config


class Command:
    """
    Command 类, 通过编程方式操作 Alembic
    """

    def __init__(self, conn_url: str) -> None:
        """
        初始化 Command 类

        Args:
            - `conn_url` (`str`): 数据库连接地址
        """
        script_location = self._script_location()

        conf = config.Config()
        # 覆盖 alembic.ini 文件中的 alembic/script_location 配置
        conf.set_main_option("script_location", script_location)

        if conn_url:
            # 覆盖 alembic.ini 文件中的 alembic/sqlalchemy.url 配置
            conf.set_main_option("sqlalchemy.url", conn_url)

        self._conf = conf

    @staticmethod
    def _script_location() -> str:
        """
        获取数据库脚本位置

        Returns:
            `str`: 数据库脚本的路径地址
        """
        curdir = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(curdir, "scripts"))

    def upgrade(self, revision: str = "head") -> None:
        """
        升级数据库

        Args:
            - `revision` (`str`, optional): 指定升级到的版本. Defaults to "head", 表示升级到最新版本.
        """
        command.upgrade(self._conf, revision)

    def downgrade(self, revision: str = "base") -> None:
        """
        降级数据库

        Args:
            - `revision` (`str`, optional): 指定降级到的版本. Defaults to "base", 表示降级到最老的版本.
        """
        command.downgrade(self._conf, revision)

    def reset(self) -> None:
        """
        重置数据库, 即降级到最后版本后重新升级到最新版本
        """
        self.downgrade()
        self.upgrade()
