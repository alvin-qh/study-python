from pdm_lib import add


def main() -> None:
    """主函式"""

    # 从标准输入中读取两个值
    print("Please input first value: ", end="")
    i1 = input()

    print("Please input second value: ", end="")
    i2 = input()

    # 从标准输入中读取值类型
    print("Please select value type [(n)umber/(s)tring]: ", end="")
    t = input()

    # 计算结果并输出到标准输出中
    match (t):
        case "n":
            result = add(int(i1), int(i2))
        case "s":
            result = add(i1, i2)
        case _:
            print("Invalid value type")
            exit(1)

    print(f"Result: {result}")


if __name__ == "__main__":
    main()
