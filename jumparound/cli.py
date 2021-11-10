from typing import List

import click
from rich import print as rprint

from . import __cli_name__, __version__
from .analyzer import Analyzer
from .config import Config
from .tui import JumpAroundApp


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command()
def to():
    JumpAroundApp.run(title=__cli_name__, log="debug.log")


@click.command()
def analyze():
    conf = Config()

    def print_callback(projects: List[str]):
        rprint(f"Found {len(projects)} projects!")
        rprint()
        rprint(projects)
        rprint()
        rprint(
            f"If any of these seem incorrectly, try updating your config located at {conf.get_full_config_file_path()}"
        )

    analyzer = Analyzer(conf)
    analyzer.run(callback=print_callback, use_cache=False)


cli.add_command(to)
cli.add_command(analyze)

if __name__ == "__main__":
    cli()
