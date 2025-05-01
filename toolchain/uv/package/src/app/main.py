from lib.func import add


def main() -> None:
    """主函数, 输入两个值, 进行加法运算"""
    s1 = input("Enter first value: ")
    s2 = input("Enter second value: ")

    opt = input("Enter an operation[(i)nt/(f)loat/(s)tr: ")
    match opt:
        case "i":
            o1 = int(s1)
            o2 = int(s2)
            ans = add(o1, o2)
        case "f":
            o1 = float(s1)
            o2 = float(s2)
            ans = add(o1, o2)
        case "s":
            o1 = s1
            o2 = s2
            ans = add(o1, o2)
        case _:
            print("Invalid operation")
            return

    print(f"The answer is {ans}")
