"""
Count the lines of code (LOC) modified in a Git repo branch in all the non-merge
 commits, authored by an author, within a start and end date, and ignoring some files.

Command line args:
    $ python -m git_loc.main <REPO-ROOT-PATH*> <BRANCH*> <FROM-DATE> <TO-DATE> <AUTHOR> <IGNORE-FILES-LIST>
    * means that the CLI arg is required.

Example:
    $ python -m git_loc.main ~/workspace/mierecensioni-be master 2020-01-01 2020-12-31 puntonim .gitignore package-lock.json
    ...
    TOTAL: 3905
"""
from datetime import datetime
from pathlib import Path
from sys import argv
from typing import Collection, Optional, Union

from .git_client import GitClient

# TODO introduce a proper cli with click.


class BaseLocCounterException(Exception):
    pass


class AuthorMismatch(BaseLocCounterException):
    pass


class FromDateMismatch(BaseLocCounterException):
    pass


class ToDateMismatch(BaseLocCounterException):
    pass


class LocCounter:
    def __init__(
        self,
        root_dir: Union[Path, str],
    ):
        self.root_dir = root_dir

    def count(
        self,
        branch: str,
        author: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        files_to_ignore: Optional[Collection] = None,
    ):
        if files_to_ignore is None:
            files_to_ignore = list()

        git_client = GitClient(self.root_dir)
        git_log = git_client.log(
            branch=branch,
            from_date=from_date,
            to_date=to_date,
            author=author,
        )

        loc_tot = 0
        # Note: we could use multi-threading here.
        for commit in git_log:
            # Ensure this commit actually matches the criteria.
            if author and author not in commit.email:
                raise AuthorMismatch
            date = datetime.strptime(commit.date, "%Y-%m-%d").date()
            if from_date and date < datetime.strptime(from_date, "%Y-%m-%d").date():
                raise FromDateMismatch
            if to_date and date > datetime.strptime(to_date, "%Y-%m-%d").date():
                raise ToDateMismatch

            # Get the diff for this commit.
            git_diff = git_client.diff(commit.hash)
            loc_in_commit = 0
            # For each file in the diff, compute the loc.
            for file_diff_stats in git_diff:
                print(file_diff_stats.path)

                # Ignore some files.
                do_ignore = False
                for file_to_ignore in files_to_ignore:
                    if file_to_ignore in file_diff_stats.path:
                        do_ignore = True
                if do_ignore:
                    print(f"\tIgnoring\n")
                    continue

                try:
                    loc_ins = int(file_diff_stats.insertions)
                    loc_in_commit += loc_ins
                except ValueError:
                    loc_ins = file_diff_stats.insertions
                    print(f"\tNo insertions value: {loc_ins}")
                try:
                    loc_del = int(file_diff_stats.deletions)
                    loc_in_commit += loc_del
                except ValueError:
                    loc_del = file_diff_stats.deletions
                    print(f"\tNo insertions value: {loc_del}")
                print(f"\t>>> Insertions #{loc_ins} | Deletions #{loc_del}\n")

            # print(f">>> Adding #{loc_in_commit} for commit {commit.hash}\n")
            loc_tot += loc_in_commit
        return loc_tot


if __name__ == "__main__":
    # Example:
    # $ python -m git_loc.main ~/workspace/mierecensioni-be master 2020-01-01 2020-12-31 puntonim .gitignore package-lock.json
    kwargs = dict(
        branch=argv[2],
        from_date=argv[3],
        to_date=argv[4],
        author=argv[5],
        files_to_ignore=argv[6:],
    )
    counter = LocCounter(root_dir=argv[1])
    loc_tot = counter.count(**kwargs)
    print(f"TOTAL LOC: {loc_tot}")
