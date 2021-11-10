from typing import List

import click
from rich import print as rprint
from rich.console import Console

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
    callback_val = None

    def on_quit_callback(val: str) -> None:
        nonlocal callback_val
        callback_val = val

    JumpAroundApp.run(
        title=__cli_name__,
        log="debug.log",
        on_quit_callback=on_quit_callback,
    )

    if callback_val:
        print(callback_val)


@click.command()
def analyze():
    conf = Config()

    def print_callback(projects: List[str]) -> None:
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
