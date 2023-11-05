import json
from datetime import date, datetime
from typing import Any, Optional


class ObjectEncoder(json.JSONEncoder):
    """
    Json 序列化扩展类
    """

    def default(self, o: Any) -> Optional[str]:
        """
        默认转换规则

        Args:
            - `obj` (`Any`): 任意对象

        Returns:
            `Optional[str]`: `None` 或字符串
        """

        s: Optional[str] = None

        # 判断如果对象是日期或时间按日期类型, 则将其转为字符串
        if isinstance(o, (date, datetime)):
            s = o.isoformat()

        # 其它类型不做转换
        return s
