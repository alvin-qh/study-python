import pretty


def error_func() -> None:
    raise Exception("This is an error")


def main() -> None:
    pretty.init()
    error_func()


if __name__ == "__main__":
    main()
