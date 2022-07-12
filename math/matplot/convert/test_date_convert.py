import random
from typing import List

import numpy as np
from matplotlib import dates as mdates
from matplotlib import pyplot as plt

from .date_convert import bytespdate2num


def test_bytespdate2num() -> None:
    """
    测试将 `bytes` 或 `bytearray` 类型的时间串转为数值
    """
    # 测试日期串
    val = bytespdate2num(b"2022-10-01")
    assert val == 19266.0

    # 测试日期时间串
    val = bytespdate2num(b"2022-10-01T12:00:00")
    assert val == 19266.5


def mock_lines_data() -> List[str]:
    lines: List[str] = []
    for d in np.arange(bytespdate2num("2020-01-01"), bytespdate2num("2022-12-31")):
        date_n = mdates.num2date(d)
        value = random.randint(-100, 300)

        if value >= 0:
            lines.append(f"{date_n},{value}")

    return sorted(lines, key=lambda s: s.split(",")[0])


def test_() -> None:
    lines = mock_lines_data()

    date, value = np.loadtxt(
        lines,
        delimiter=',',
        unpack=True,
        converters={
            0: bytespdate2num,
        }
    )

    plt.plot_date(date, value, '-', label='Price')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Interesting Graph\nCheck it out')
    plt.legend()
    plt.show()
