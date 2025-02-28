"""command-line interface for eatlocal

"""

import sys

from collections import namedtuple
from pathlib import Path

import typer

from .constants import USERNAME, PASSWORD
from .eatlocal import extract_bite, submit_bite, download_bite

from . import __version__


cli = typer.Typer(add_completion=False)


def report_version(display: bool) -> None:
    """Print version and exit."""
    if display:
        print(f"{Path(sys.argv[0]).name} {__version__}")
        raise typer.Exit()


GlobalOptions = namedtuple("GlobalOptions", "creds")


@cli.callback()
def global_options(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        is_flag=True,
        is_eager=True,
        callback=report_version,
    ),
):
    """Download, extract and submit PyBites code challenges."""

    ctx.obj = GlobalOptions((USERNAME, PASSWORD))


@cli.command(name="download")
def download_subcommand(
    ctx: typer.Context,
    bite_number: int,
    cleanup: bool = typer.Option(
        False,
        "--cleanup",
        "-C",
        is_flag=True,
        help="Remove downloaded bite archive file.",
    ),
) -> None:
    """Download and extract bite code from Codechalleng.es.

    The bites are downloaded in a zip archive file and unzipped
    in the current directory. If the `cleanup` option is present
    the archive is deleted after extraction.
    """
    download_bite(bite_number, *ctx.obj.creds, cache_path="cache")
    extract_bite(bite_number, cleanup=cleanup, cache_path="cache")


@cli.command(name="submit")
def submit_subcommand(
    ctx: typer.Context,
    bite_number: int,
) -> None:
    """Submit a bite back to Codechalleng.es."""

    submit_bite(bite_number, *ctx.obj.creds)


if __name__ == "__main__":
    cli()
