from invoke.context import Context
from invoke.tasks import task


@task
def type(c: Context) -> None:
    c.run("uv run mypy")
    c.run("uv run --directory packages/lib mypy")
    c.run("uv run --directory packages/utils mypy")


@task
def lint(c: Context) -> None:
    c.run("uv run pycln --config pyproject.toml")
    c.run("uv run --directory packages/lib pycln --config pyproject.toml")
    c.run("uv run --directory packages/utils pycln --config pyproject.toml")

    c.run("uv run autopep8 .")
    c.run("uv run --directory packages/lib autopep8 .")
    c.run("uv run --directory packages/utils autopep8 .")


@task
def test(c: Context) -> None:
    c.run("uv run pytest")
    c.run("uv run --directory packages/lib pytest")
    c.run("uv run --directory packages/utils pytest")


@task(pre=[type, lint, test])
def check(c: Context) -> None:
    pass


@task
def clean(c: Context) -> None:
    c.run("python clear.py")


@task
def start(c: Context) -> None:
    c.run("python main.py")


@task
def type_install(c: Context) -> None:
    c.run("mypy --install-types")
