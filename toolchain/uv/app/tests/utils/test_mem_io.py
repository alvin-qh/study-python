from utils import stdin_redirected, stdout_redirected


def test_redirect_stdout() -> None:
    """测试重定向标准输出"""
    # 重定向标准输出到一个 `StringIO` 对象
    with stdout_redirected() as stdout:
        # 通过标准输出输出一些文本
        print("Hello, World!")

        # 确认标准输出内容符合预期
        assert stdout.getvalue() == "Hello, World!\n"


def test_redirect_stdin() -> None:
    """测试重定向标准输入"""
    # 用于输入到标准输入的文本, 每次输入通过 `\n` 分割
    input_text = """Hello, World!
Welcome to Python!
"""

    # 将 `input_text` 变量中存储的文本作为重定向的标准输入
    with stdin_redirected(input_text):
        # 通过标准输入输入第一段文本
        input_str = input()
        # 确认输入的内容符合预期
        assert input_str == "Hello, World!"

        # 通过标准输入输入第二段文本
        input_str = input()
        # 确认输入的内容符合预期
        assert input_str == "Welcome to Python!"
