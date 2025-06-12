from invoke.tasks import task
from invoke.context import Context


@task
def lint(c: Context) -> None:
    c.run("autopep8 .")
    c.run("pycln --config pyproject.toml")


@task
def type(c: Context) -> None:
    c.run("mypy")


@task
def test(c: Context) -> None:
    c.run("pytest")


@task(pre=[lint, type, test])
def check(c: Context) -> None:
    pass
