import subprocess
from collections import namedtuple
from pathlib import Path
from typing import Iterator, Optional, Union

GIT_LOG_BIN = "git"  # Or: "/usr/local/bin/git".
GIT_DIFF_BIN = GIT_LOG_BIN
DO_USE_POPEN_SHELL = False


GitLogEntry = namedtuple("GitLogEntry", ("hash", "date", "email", "summary"))
GitDiffEntry = namedtuple("GitDiffEntry", ("insertions", "deletions", "path"))


class GitClient:
    def __init__(self, root_dir: Union[Path, str]):
        self.root_dir = root_dir

    def _run_git_process(self, git_base_cmd, *args):
        run_args = (git_base_cmd,) + args
        if DO_USE_POPEN_SHELL:
            run_args = " ".join(run_args)
        return subprocess.run(
            run_args, cwd=self.root_dir, capture_output=True, shell=DO_USE_POPEN_SHELL
        )

    def log(
        self,
        branch: str,
        author: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Iterator[GitLogEntry]:
        # Ref. command:
        # $ git log master \
        #   --pretty=format:"%h %ad %ae %s%d" \
        #   --date=short \
        #   --no-merges \
        #   --since="2021-01-01" \
        #   --before="2021-12-31" \
        #   --author="paolo"
        run_args = [
            "log",
            branch,
            "--pretty=format:'%h %ad %ae %s%d'",
            "--date=short",
            "--no-merges",
        ]
        if from_date:
            run_args.append(f"--since='{from_date}'")
        if to_date:
            run_args.append(f"--before='{to_date}'")
        if author:
            # No need to use quotes even if `author` includes a whitespace.
            run_args.append(f"--author={author}")
        result = self._run_git_process(GIT_LOG_BIN, *run_args)
        for commit in result.stdout.decode("utf-8").split("\n"):
            if not commit:
                continue
            tokens: str = commit.split(" ")
            # Tokens is a string like:
            # 2fdffa2 2020-02-10 foo@gmail.com NEW Enable CORS for qa.mierecensioni.it (HEAD -> master, origin/master)
            yield GitLogEntry(
                hash=tokens[0][1:],  # Slice to remove the initial quote.
                date=tokens[1],
                email=tokens[2],
                # Combine summary (subject in Git terms) and ref name, but remove the
                #  ending quote.
                summary=" ".join(tokens[3:])[:-1],
            )

    def diff(self, hash: str) -> Iterator[GitDiffEntry]:
        # Ref. command:
        # $ git diff --numstat 2fdffa2~1 2fdffa2
        result = self._run_git_process(
            GIT_DIFF_BIN, "diff", "--numstat", f"{hash}~1", hash
        )
        for file_diff_stats in result.stdout.decode("utf-8").split("\n"):
            if not file_diff_stats:
                continue
            tokens: str = file_diff_stats.split("\t")
            # Tokens is a string like:
            # 31	10	git_loc/main.py
            yield GitDiffEntry(
                insertions=tokens[0],
                deletions=tokens[1],
                path=tokens[2],
            )
