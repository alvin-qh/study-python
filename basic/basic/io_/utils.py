def read_file_first_line(filename: str, encoding: str = "utf-8") -> str:
    """读取文件内容的第一行

    Args:
        - `filename` (`str`): 要读取的文件名

    Returns:
        `str`: 文件内容第一行
    """
    with open(filename, "r", encoding=encoding) as pf:
        return pf.readline()


def compare_file(file_a: str, file_b: str) -> bool:
    """比较两个文件是否相同

    Args:
        - `file_a` (`str`): 第一个文件名
        - `file_b` (`str`): 第二个文件名

    Returns:
        `bool`: 是否相同
    """
    with open(file_a, "rb") as fa:
        with open(file_b, "rb") as fb:
            return fa.read() == fb.read()
