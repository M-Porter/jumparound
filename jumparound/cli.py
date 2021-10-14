from jumparound.config import Config
from jumparound.analyzer import Analyzer
import click
from .tui import JumpAroundApp
from . import __cli_name__


@click.group()
def cli():
    pass


@click.command()
def to():
    JumpAroundApp.run(title=__cli_name__, log="debug.log")


@click.command()
def analyze():
    analyzer = Analyzer(Config())
    analyzer.run(debug=True)


cli.add_command(to)
cli.add_command(analyze)

if __name__ == "__main__":
    cli()
