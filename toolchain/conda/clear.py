import glob
import os
import shutil


_FILE_PATTERNS = [
    "**/__pycache__",
    "**/.hypothesis",
    "**/.mypy_cache",
    "**/.pytest_cache",
    ".wheelhouse"
]


def main() -> None:
    for pattern in _FILE_PATTERNS:
        files = glob.glob(pattern, recursive=True)
        for file in files:
            if os.path.isfile(file):
                print(f"Remove file {file}")
                os.remove(file)
            else:
                print(f"Remove directory {file}")
                shutil.rmtree(file, ignore_errors=True)


if __name__ == "__main__":
    main()
