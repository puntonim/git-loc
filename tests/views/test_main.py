from datetime import datetime

import pytest

from git_loc.clients.git_client import NotADate
from git_loc.domains.main import AuthorMismatch, EndDateMismatch, StartDateMismatch
from git_loc.utils.printer import remove_ansi_chars
from git_loc.views.main import _count, count

from ..testfactories.git_log_factory import (
    GitDiffEntry,
    GitDiffFactory,
    GitLogEntry,
    GitLogFactory,
)
from ..testutils.settings_testutils import override_settings


class TestCount:
    def setup(self):
        self.git_log_entry1 = GitLogEntry(
            hash="1111111",
            date="2020-02-10",
            email="john@gmail.com",
            summary="NEW Enable CORS for qa.mierecensioni.it (HEAD -> master, origin/master)",
        )
        self.git_diff_entry1 = GitDiffEntry(
            insertions="10",
            deletions="2",
            path="/tmp1",
        )
        self.git_diff_entry2 = GitDiffEntry(
            insertions="11",
            deletions="3",
            path="/tmp2",
        )
        self.start_date = datetime(2020, 2, 1)
        self.end_date = datetime(2020, 3, 1)

    def test_happy_flow(self):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            loc_tot = count(
                root_dir="/tmp",
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
                # files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 26

    def test_two_commits(self):
        git_log_entry2 = GitLogEntry(
            hash="2222222",
            date="2020-02-11",
            email="john@gmail.com",
            summary="NEW Answer model",
        )
        with GitLogFactory((self.git_log_entry1, git_log_entry2)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            loc_tot = count(
                root_dir="/tmp",
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
                # files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 52

    def test_no_insertions(self):
        git_diff_entry3 = GitDiffEntry(
            insertions="-",
            deletions="1",
            path="/tmp1",
        )
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2, git_diff_entry3)
        ):
            loc_tot = count(
                root_dir="/tmp",
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
                # files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 27

    def test_no_deletions(self):
        git_diff_entry3 = GitDiffEntry(
            insertions="1",
            deletions="-",
            path="/tmp1",
        )
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2, git_diff_entry3)
        ):
            loc_tot = count(
                root_dir="/tmp",
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
                # files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 27

    def test_ignored_file(self):
        git_diff_entry3 = GitDiffEntry(
            insertions="1",
            deletions="9",
            path="/tmp/.gitignore",
        )
        git_diff_entry4 = GitDiffEntry(
            insertions="1",
            deletions="11",
            path="/tmp/package-lock.json",
        )
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (
                self.git_diff_entry1,
                self.git_diff_entry2,
                git_diff_entry3,
                git_diff_entry4,
            )
        ):
            loc_tot = count(
                root_dir="/tmp",
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
                files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 26

    def test_author_mismatch(self):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(AuthorMismatch):
                count(
                    root_dir="/tmp",
                    branch="master",
                    start_date=self.start_date,
                    end_date=self.end_date,
                    author="XXX",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )

    def test_start_date_mismatch(self):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(StartDateMismatch):
                count(
                    root_dir="/tmp",
                    branch="master",
                    start_date=datetime(2021, 2, 1),
                    end_date=datetime(2021, 3, 1),
                    author="john",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )

    def test_start_date_string(self):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(NotADate):
                count(
                    root_dir="/tmp",
                    branch="master",
                    start_date="XXX",
                    end_date=datetime(2021, 3, 1),
                    author="john",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )

    def test_end_date_mismatch(self):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(EndDateMismatch):
                count(
                    root_dir="/tmp",
                    branch="master",
                    start_date=datetime(2020, 2, 1),
                    end_date=datetime(2020, 2, 1),
                    author="john",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )

    def test_end_date_string(self):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(NotADate):
                count(
                    root_dir="/tmp",
                    branch="master",
                    start_date=datetime(2020, 2, 1),
                    end_date="XXX",
                    author="john",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )


class TestCli:
    def setup(self):
        self.git_log_entry1 = GitLogEntry(
            hash="1111111",
            date="2020-02-10",
            email="john@gmail.com",
            summary="NEW Enable CORS for qa.mierecensioni.it (HEAD -> master, origin/master)",
        )
        self.git_diff_entry1 = GitDiffEntry(
            insertions="10",
            deletions="2",
            path="/tmp1",
        )
        self.git_diff_entry2 = GitDiffEntry(
            insertions="11",
            deletions="3",
            path="/tmp2",
        )
        self.start_date = "2020-02-01"
        self.end_date = "2020-03-01"

    @override_settings(DO_SUPPRESS_PRINT=False)
    def test_happy_flow(self, cli_runner):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            result = cli_runner.invoke(
                _count,
                [
                    "--dir=/tmp",
                    "--branch=master",
                    f"--start-date={self.start_date}",
                    f"--end-date={self.end_date}",
                    "--author=john",
                    "--ignore-file=package-lock.json",
                ],
            )

        assert result.exit_code == 0
        stdout = remove_ansi_chars(result.stdout).strip().split("\n")
        assert stdout[-1] == "LOC: 26"

    @override_settings(DO_SUPPRESS_PRINT=False)
    def test_all_missing(self, cli_runner):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            result = cli_runner.invoke(
                _count,
                input=f"/tmp\nmaster\njohn\n{self.start_date}\n{self.end_date}\npackage-lock.json;.gitignore\n",
            )
        assert result.exit_code == 0
        stdout = remove_ansi_chars(result.stdout).strip().split("\n")
        assert stdout[-1] == "LOC: 26"

    @override_settings(DO_SUPPRESS_PRINT=False)
    def test_dir_missing(self, cli_runner):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            result = cli_runner.invoke(
                _count,
                [
                    # "--dir=/tmp",
                    "--branch=master",
                    f"--start-date={self.start_date}",
                    f"--end-date={self.end_date}",
                    "--author=john",
                    "--ignore-file=package-lock.json",
                ],
                input="/tmp\n",
            )

        assert result.exit_code == 0
        stdout = remove_ansi_chars(result.stdout).strip().split("\n")
        assert stdout[-1] == "LOC: 26"

    @override_settings(DO_SUPPRESS_PRINT=False)
    def test_dir_and_author_missing(self, cli_runner):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            result = cli_runner.invoke(
                _count,
                [
                    # "--dir=/tmp",
                    "--branch=master",
                    f"--start-date={self.start_date}",
                    f"--end-date={self.end_date}",
                    # "--author=john",
                    "--ignore-file=package-lock.json",
                ],
                input=f"/tmp\njohn\n",
            )

        assert result.exit_code == 0
        stdout = remove_ansi_chars(result.stdout).strip().split("\n")
        assert stdout[-1] == "LOC: 26"

    @override_settings(DO_SUPPRESS_PRINT=False)
    def test_start_date_invalid(self, cli_runner):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            result = cli_runner.invoke(
                _count,
                [
                    # "--dir=/tmp",
                    "--branch=master",
                    # f"--start-date={self.start_date}",
                    f"--end-date={self.end_date}",
                    "--author=john",
                    "--ignore-file=package-lock.json",
                ],
                input=f"/tmp\nXXX\n",
            )

        assert result.exit_code == 1
        assert "Not a valid date" in result.stdout

    @override_settings(DO_SUPPRESS_PRINT=False)
    def test_end_date_invalid(self, cli_runner):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            result = cli_runner.invoke(
                _count,
                [
                    # "--dir=/tmp",
                    "--branch=master",
                    f"--start-date={self.start_date}",
                    # f"--end-date={self.end_date}",
                    "--author=john",
                    "--ignore-file=package-lock.json",
                ],
                input=f"/tmp\nXXX\n",
            )

        assert result.exit_code == 1
        assert "Not a valid date" in result.stdout

    @override_settings(DO_SUPPRESS_PRINT=False)
    def test_ignore_file_many(self, cli_runner):
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            result = cli_runner.invoke(
                _count,
                [
                    # "--dir=/tmp",
                    "--branch=master",
                    f"--start-date={self.start_date}",
                    f"--end-date={self.end_date}",
                    "--author=john",
                    # "--ignore-file=package-lock.json",
                ],
                input=f"/tmp\npackage-lock.json;.gitignore\n",
            )

        assert result.exit_code == 0
        stdout = remove_ansi_chars(result.stdout).strip().split("\n")
        assert stdout[-2] == "Ignored files: ['package-lock.json', '.gitignore']"
        assert stdout[-1] == "LOC: 26"
