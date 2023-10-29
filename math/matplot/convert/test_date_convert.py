import random
from typing import List, Tuple

import numpy as np
from matplotlib import dates as mdates  # type: ignore
from matplotlib import pyplot as plt

from .date_convert import bytespdate2num


def test_bytespdate2num() -> None:
    """
    测试将 `bytes` 或 `bytearray` 类型的时间串转为 `float` 型数值
    """
    # 测试日期串
    val = bytespdate2num(b"2022-10-01")
    assert val == 19266.0

    # 测试日期时间串
    val = bytespdate2num(b"2022-10-01T12:00:00")
    assert val == 19266.5


def mock_lines_data() -> List[str]:
    """
    构造测试数据

    Returns:
        List[str]: 测试数据列表
    """
    # 随机产生阶段最大值
    max_ = random.randint(100, 300)

    # 随机产生阶段最小值
    value = min_ = random.randint(max_ // 2, max_)

    # 增长值
    n = 1

    lines: List[str] = []

    # 遍历指定日期区间, 为每一天产生一条数据
    for d in np.arange(bytespdate2num("2018-01-01"), bytespdate2num("2022-12-31")):
        # 产生日期数据
        date_n = mdates.num2date(d)

        # 产生一条数据
        lines.append(f"{date_n},{value}")

        # 根据数据增长情况, 定义下阶段数据范围
        if value > max_:
            n = -1
            min_ = random.randint(0, max_)
        elif value < min_:
            n = 1
            max_ = random.randint(200, 300)

        # 令数据产生变化
        value += n

    return lines


def test_date_convert() -> None:
    """
    测试日期类型转换

    通过 numpy 的 `loadtxt` 函数, 设置 `converters` 参数指定转换器,
    将 `bytes` 类型时间日期串转为 `float` 类型
    """
    lines = mock_lines_data()

    # 读取数据, 每条数据用 "," 分割, 产生 date 和 value 两组数据
    date, value = np.loadtxt(
        lines,
        delimiter=",",  # 设置分割符
        unpack=True,  # 返回多个变量
        converters={
            0: bytespdate2num,  # 设定日期转换函数
        }
    )

    # 设置 x 和 y 坐标轴的标签
    plt.xlabel("Date")
    plt.ylabel("Value")

    # 绘制日期折线图
    plt.plot_date(  # type: ignore
        date,  # 日期
        value,  # 数据
        "r-",  # 绘图格式, 绘制实线
        label="Value",
        xdate=True,
        ydate=False,
    )

    # 绘制图例
    plt.legend()

    # 显示绘图
    plt.show()
