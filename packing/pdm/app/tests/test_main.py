import io
import sys

from pdm_app.app import main


def test_main() -> None:
    stdin_ = sys.stdin
    stdout_ = sys.stdout

    try:
        with io.StringIO("10\n20\ns\n") as in_:
            with io.StringIO() as out_:
                sys.stdin = in_
                sys.stdout = out_

                main()

                assert out_.getvalue() == (
                    "Please input first value: Please input second value: "
                    "Please select value type [(n)umber/(s)tring]: Result: 1020\n"
                )

        with io.StringIO("10\n20\nn\n") as in_:
            with io.StringIO() as out_:
                sys.stdin = in_
                sys.stdout = out_

                main()

                assert out_.getvalue() == (
                    "Please input first value: Please input second value: "
                    "Please select value type [(n)umber/(s)tring]: Result: 30\n"
                )
    finally:
        sys.stdin = stdin_
        sys.stdout = stdout_
