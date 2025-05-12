from lib import stdin_redirected, stdout_redirected
from main import main


def test_main() -> None:
    """测试 `main.py` 下的 `main` 函数"""
    # 重定向标准输入, 依次输入 `1`, `2`, `n` 三个字符串
    with stdin_redirected("1\n2\nn\n"):

        # 重定向标准输出到一个 `StringIO` 对象
        with stdout_redirected() as s_io:

            # 执行 `main` 函数
            main()

            # 确认标准输出的内容符合预期
            assert s_io.getvalue() == (
                "Please input first value: "
                "Please input second value: "
                "Please select value type [(n)umber/(s)tring]: "
                "Result: 3\n"
            )
