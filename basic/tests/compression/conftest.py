from pathlib import Path
from typing import Any, Generator, cast

from _pytest.fixtures import SubRequest
from pytest import fixture


@fixture
def delete_file_fixture(request: SubRequest) -> Generator[list[str], None, None]:
    """创建一个 pytest fixture, 起到如下几个作用:

    1. 自动生成临时文件的文件名, 可根据传入参数的 `extension` 值设置文件扩展名; 可根据传入参数的 `count` 值, 生成指定数量的文件名

    该 fixture 可根据传入的参数的 `extension` 属性值, 自动生成所需的文件名, 允许通过 `request` 参数的 `.param` 属性, 传入文件名或扩展名配置，
    在测试结束后自动删除这些文件， 以确保测试环境的清洁

    参数:
        request: SubRequest对象，包含传递给fixture的参数信息
                 可能的参数包括:
                   - extension: 文件扩展名，默认为".gz"
                   - file_names: 文件名列表，可以是字符串、列表、元组或集合

    返回:
        Generator[list[str], None, None]: 生成一个包含待删除文件名的列表
    """
    param = cast(dict[str, Any], request.param)

    # 获取文件扩展名，默认为.gz
    ext = cast(str, param.get("extension", ".gz"))

    # 获取要生成的文件名数量
    count = cast(int, param.get("count", 1))

    # 如果 count 值大于 1, 则生成多个文件名, 否则生成一个文件名
    if count > 1:
        file_names = [
            f"{request.node.originalname}-{i}{ext}"  # pyright: ignore[reportAttributeAccessIssue]
            for i in range(1, count + 1)
        ]
    else:
        file_names = [
            f"{request.node.originalname}{ext}"  # pyright: ignore[reportAttributeAccessIssue]
        ]

    yield file_names

    # 测试完成后，删除所有指定的文件
    for file_name in file_names:
        Path(file_name).unlink(missing_ok=True)
