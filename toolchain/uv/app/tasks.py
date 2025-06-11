from invoke.tasks import task
from invoke.context import Context


@task
def type(c: Context) -> None:
    c.run("mypy")


@task
def lint(c: Context) -> None:
    c.run("pycln --config pyproject.toml")
    c.run("autopep8 .")


@task
def test(c: Context) -> None:
    c.run("pytest")


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
