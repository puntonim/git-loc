from datetime import datetime
from pathlib import Path
from typing import Collection, Optional

import click
from rich.prompt import Prompt

from ..domains.main import LocCounter
from ..utils import command, printer

console = printer.ConsoleAdapter()


@click.command(cls=command.BaseCommand, name="count")
@click.option(
    "--dir",
    "root_dir",
    required=False,
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="Git root dir.",
)
@click.option(
    "--branch",
    required=False,
    type=str,
    help="Git branch.",
)
@click.option(
    "--start-date",
    required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Commit start date.",
)
@click.option(
    "--end-date",
    required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Commit end date.",
)
@click.option(
    "--author",
    required=False,
    type=str,
    help="Commit author name or email.",
)
@click.option(
    "--ignore-file",
    "files_to_ignore",
    required=False,
    type=str,
    multiple=True,
    help="Ignore file.",
)
def _count(
    root_dir: str,
    branch: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    author: Optional[str] = None,
    files_to_ignore: Optional[list[str]] = None,
) -> None:
    """
    Count LOC in a Git repo branch.
    """
    count(root_dir, branch, start_date, end_date, author, files_to_ignore)


def count(
    root_dir: str,
    branch: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    author: Optional[str] = None,
    files_to_ignore: Optional[list[str]] = None,
) -> int:
    all_options = dict(
        root_dir=root_dir,
        branch=branch,
        start_date=start_date,
        end_date=end_date,
        author=author,
        files_to_ignore=files_to_ignore,
    )

    prompted_options = dict()
    if not root_dir or not branch:
        prompted_options = _prompt_for_all_options(all_options)

    all_options.update(**prompted_options)

    counter = LocCounter(all_options["root_dir"])
    tot = counter.count(
        branch=all_options["branch"],
        start_date=all_options["start_date"],
        end_date=all_options["end_date"],
        author=all_options["author"],
        files_to_ignore=all_options["files_to_ignore"],
    )

    console.print(f"\nRepo root dir: {all_options['root_dir']}")
    console.print(f"Branch: {all_options['branch']}")
    console.print(f"Author: {all_options['author']}")
    console.print(f"Start date: {all_options['start_date'].date()}")
    console.print(f"End date: {all_options['end_date'].date()}")
    console.print(f"Ignored files: {all_options['files_to_ignore']}")
    console.print(f"[bold blue on yellow2]LOC: {tot}\n")
    return tot


def _prompt_for_all_options(cli_options) -> dict:
    options = dict()

    # Prompt for root_dir.
    root_dir = cli_options.get("root_dir")
    if root_dir is None:
        root_dir = _prompt_for_root_dir()
    options["root_dir"] = root_dir

    # Prompt for branch.
    branch = cli_options.get("branch")
    if branch is None:
        branch = _prompt_for_branch()
    options["branch"] = branch

    # Prompt for author.
    author = cli_options.get("author")
    if author is None:
        author: str = _prompt_for_author()
    options["author"] = author or None

    # Prompt for start_date.
    start_date = cli_options.get("start_date")
    if start_date is None:
        start_date = _prompt_for_date("start date")
    options["start_date"] = start_date or None

    # Prompt for end_date.
    end_date = cli_options.get("end_date")
    if end_date is None:
        end_date = _prompt_for_date("end date")
    options["end_date"] = end_date or None

    # Prompt for files_to_ignore.
    files_to_ignore = cli_options.get("files_to_ignore")
    if files_to_ignore is None or not len(files_to_ignore):
        files_to_ignore = _prompt_for_files_to_ignore()
    options["files_to_ignore"] = files_to_ignore or None

    return options


def _prompt_for_root_dir() -> Path:
    prompt_text = "Git [underline]root dir"
    root_dir: str = Prompt.ask(prompt_text)
    while not root_dir or not Path(root_dir).is_dir():
        if root_dir:
            console.print(f"[red]Directory '{root_dir}' does not exist")
        root_dir: str = Prompt.ask(prompt_text)
    return Path(root_dir)


def _prompt_for_branch() -> str:
    prompt_text = "Git [underline]branch"
    branch: str = Prompt.ask(prompt_text)
    while not branch:
        branch: str = Prompt.ask(prompt_text)
    return branch


def _prompt_for_author() -> Optional[str]:
    author: str = Prompt.ask(
        "Commits [underline]author[/] name or email \\[not required]"
    )
    return author or None


def _prompt_for_date(date_description: str) -> Optional[datetime]:
    prompt_text = (
        f"Commits [underline]{date_description}[/] (eg.: 2020-01-12) \\[not required]"
    )
    is_valid_input = False
    while not is_valid_input:
        date: str = Prompt.ask(prompt_text)
        if not date:
            return None
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
            is_valid_input = True
        except ValueError:
            console.print(f"[red]Not a valid date (eg.: 2020-01-12)")
    return date


def _prompt_for_files_to_ignore() -> Optional[Collection]:
    files_to_ignore: str = Prompt.ask(
        "File names [underline]to ignore[/] (use ; as separator) \\[not required]"
    )
    if files_to_ignore:
        files_to_ignore = [x.strip() for x in files_to_ignore.split(";")]
    return files_to_ignore or None
