from pytest import mark


@mark.webtest
def test_custom_markers() -> None:
    """
    自定义标记:
    - 可以使用命令 `pytest -m <custom marker>` 执行指定自定义标记的测试用例
    - 所有使用的自定义标记, 都应该在 `pytest.ini` 文件中进行声明

    ```ini
    [pytest]
    markers =
        webtest: Test cases for website
    ```
    """
