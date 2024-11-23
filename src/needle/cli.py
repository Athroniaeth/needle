import typer
from typer import Typer

cli = Typer()


@cli.command()
def hello(name: str):
    """Say hello to NAME."""
    typer.echo(f"Hello {name}!")


@cli.command()
def hello_world():
    """Say hello to the world."""
    hello(name="World")
