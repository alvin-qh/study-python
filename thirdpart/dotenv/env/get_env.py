import os
from typing import Dict, Optional

from dotenv import dotenv_values

# 从 .env 文件和环境变量中加载配置信息
CONFIG: Dict[str, Optional[str]] = {
    **dotenv_values(".env"),  # 加载 .env 文件中的变量
    **os.environ,  # 加载操作系统环境变量, 其中的值会覆盖 .env 文件中的值
}


def get_env(key: str) -> Optional[str]:
    """根据 Key 获取环境变量中的值

    Args:
        - `key` (`str`): 环境变量的名称 (Key)

    Returns:
        `Optional[str]`: 环境变量的值, `None` 表示不存在
    """
    return CONFIG.get(key, None)
