from datetime import datetime
from pathlib import Path
from typing import Collection, Optional

from rich.table import Table

from ..clients.git_client import GitClient
from ..utils import printer


class BaseLocCounterException(Exception):
    pass


class AuthorMismatch(BaseLocCounterException):
    pass


class StartDateMismatch(BaseLocCounterException):
    pass


class EndDateMismatch(BaseLocCounterException):
    pass


console = printer.ConsoleAdapter()


class LocCounter:
    def __init__(self, root_dir: Path | str):
        """
        Count the lines of code (LOC) modified in a Git repo branch in all the non-merge
         commits, authored by an author, within a start and end date, and ignoring
         some files.
        """
        self.root_dir = root_dir

    def count(
        self,
        branch: str,
        author: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        files_to_ignore: Optional[Collection] = None,
    ):
        console.print("Computing...")
        table = Table(title="[bold underline]Files[/]")
        table.add_column("insertions")
        table.add_column("deletions")
        table.add_column("file path", overflow="fold")

        if files_to_ignore is None:
            files_to_ignore = list()

        git_client = GitClient(self.root_dir)
        git_log = git_client.log(
            branch=branch,
            start_date=start_date,
            end_date=end_date,
            author=author,
        )

        loc_tot = 0
        # Note: we could use multi-threading here.
        for commit in git_log:
            # Ensure this commit actually matches the criteria.
            if author and author not in commit.email:
                raise AuthorMismatch
            date = datetime.strptime(commit.date, "%Y-%m-%d").date()
            if start_date and date < start_date.date():
                raise StartDateMismatch
            if end_date and date > end_date.date():
                raise EndDateMismatch

            # Get the diff for this commit.
            git_diff = git_client.diff(commit.hash)
            loc_in_commit = 0
            # For each file in the diff, compute the loc.
            for file_diff_stats in git_diff:
                # Ignore some files.
                do_ignore = False
                for file_to_ignore in files_to_ignore:
                    if file_to_ignore in file_diff_stats.path:
                        do_ignore = True
                if do_ignore:
                    table.add_row("ignored", "ignored", file_diff_stats.path)
                    continue

                try:
                    loc_ins = int(file_diff_stats.insertions)
                    loc_in_commit += loc_ins
                except ValueError:
                    loc_ins = file_diff_stats.insertions
                try:
                    loc_del = int(file_diff_stats.deletions)
                    loc_in_commit += loc_del
                except ValueError:
                    loc_del = file_diff_stats.deletions

                table.add_row(str(loc_ins), str(loc_del), file_diff_stats.path)

            loc_tot += loc_in_commit

        console.print(table)
        return loc_tot
