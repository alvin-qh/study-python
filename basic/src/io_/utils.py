def read_file_first_line(filename: str, encoding: str = "utf-8") -> str:
    """
    读取文件内容的第一行

    Args:
        filename (str): 要读取的文件名

    Returns:
        str: 文件内容第一行
    """
    with open(filename, "r", encoding=encoding) as pf:
        return pf.readline()
