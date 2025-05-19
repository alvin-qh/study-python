from setuptools import setup, find_packages

from os import path

# 获取当前目录
CURRENT_DIR = path.abspath(path.dirname(__file__))


def load_readme() -> str:
    """加载当前目录下的 `README.md` 文件

    Returns:
        str: `README.md` 文件内容
    """
    with open(path.join(CURRENT_DIR, "README.md"), "r", encoding="utf-8") as f:
        return f.read()


# 执行 `setup` 函数, 打包当前项目
setup(
    name="toolchain-setup",
    version="0.0.1",
    classifiers=[
        "Development Status :: 3 - Production",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Setup toolchain demo",
    author="Alvin",
    author_email="quhao317@163.com",
    license="MIT",
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["toolchain_setup"]),
    package_dir={"": "."},
    include_package_data=True,
    package_data={
        "toolchain_setup": [
            "conf/*.json",
        ],
    },
    install_requires=[
        "click>=8.1.8",
    ],
    extras_require={
        "test": [
            "pytest>=8.3.5",
            "pytest-sugar>=1.0.0",
        ],
        "type": [
            "mypy>=1.15.0",
            "mypy_extensions>=1.1.0",
        ],
        "lint": [
            "autopep8>=2.3.2",
            "pycln>=2.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "toolchain-setup=toolchain_setup.main:main",
        ],
    },
)
