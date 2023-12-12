from logging import Formatter, LogRecord
from typing import Dict, Literal, Optional, TypeAlias

FormatStyle: TypeAlias = Literal["%", "{", "$"]


class RequestFormatter(Formatter):
    """自定义日志格式化器"""

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: FormatStyle = "%",
        extra: Optional[Dict[str, str]] = None,
    ) -> None:
        """初始化格式化器

        Args:
            - `fmt` (`Optional[str]`, optional): 日志格式化模板. Defaults to `None`.
            - `datefmt` (`Optional[str]`, optional): 日期格式化模板. Defaults to `None`.
            - `style` (`str`, optional): 日志模板中变量的前缀字符串. Defaults to `"%"`.
            - `extra` (`Optional[Dict[str, str]]`, optional): 扩展参数. Defaults to `None`.
        """
        super().__init__(fmt, datefmt, style)
        self._extra = extra

    def format(self, record: LogRecord) -> str:
        """格式化日志内容

        Args:
            - `record` (`LogRecord`): 日志内容对象, 表示一条日志

        Returns:
            `str`: 格式化后的日志字符串
        """
        # 可以为 record 对象增加自定义变量的值
        # 自定义变量可以通过日志模板中的 %(<变量名>)s 进行替换输出
        if self._extra:
            # 遍历 extera 字典
            for k, v in self._extra.items():
                # 将字典的键值对作为扩展变量设置到日志对象上
                record.__setattr__(k, v)

        return super().format(record)
