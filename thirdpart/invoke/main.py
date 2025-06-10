import sys
import colorama as cm

cm.init()


def main() -> None:
    fg = ""
    bg = ""
    style = ""

    for i in range(1, len(sys.argv)):
        match sys.argv[1]:
            case "--force" | "-f":
                fg = cm.Fore.BLACK


if __name__ == "__main__":
    main()
