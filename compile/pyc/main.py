from pyc.app import app
from pyc.utils.paths import watch_files_for_develop


def main() -> None:
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )


if __name__ == "__main__":
    main()
