from typing import List, Union

import click
from rich import print as rprint
from rich.console import Console
from rich.syntax import Syntax

from . import __cli_name__, __version__
from .analyzer import Analyzer, Project
from .config import Config
from .tui import JumpAroundApp


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command()
def to():
    callback_val: Union[Project, None] = None

    def on_quit_callback(val: Union[Project, None]) -> None:
        nonlocal callback_val
        callback_val = val

    console = Console(
        force_terminal=True,
        force_interactive=False,
        stderr=True,
        highlight=False,
    )

    JumpAroundApp.run(
        title=__cli_name__,
        console=console,
        on_quit_callback=on_quit_callback,
    )

    if callback_val:
        print(callback_val.path)


@click.command()
def analyze():
    conf = Config()

    def print_callback(projects: List[Project]) -> None:
        for p in projects:
            rprint(f"{p.name}: {p.path}")
        rprint()
        rprint(
            f"Found {len(projects)} projects! If any of these seem incorrect, try updating your config located at {conf.get_full_config_file_path()} or by running [code]jumparound edit-config[/code]."
        )

    analyzer = Analyzer(conf)
    analyzer.run(callback=print_callback, use_cache=False)


@click.command()
def print_config():
    s = Syntax(Config().dump(), "yaml", dedent=True, background_color=None)
    c = Console()
    c.print(s)


cli.add_command(to)
cli.add_command(analyze)
cli.add_command(print_config)


if __name__ == "__main__":
    cli()
