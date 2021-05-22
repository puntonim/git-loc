from datetime import datetime

import pytest

from git_loc.clients.git_client import GitClient, NotADate

from ..testfactories.git_log_factory import (
    GitDiffEntry,
    GitDiffFactory,
    GitLogEntry,
    GitLogFactory,
)


class TestLog:
    def setup(self):
        self.git_log_entry1 = GitLogEntry(
            hash="2fdffa2",
            date="2020-02-10",
            email="foo@gmail.com",
            summary="NEW Enable CORS for qa.mierecensioni.it (HEAD -> master, origin/master)",
        )
        self.git_log_entry2 = GitLogEntry(
            hash="7hdff09",
            date="2020-02-09",
            email="foo@gmail.com",
            summary="NEW Answer model",
        )
        self.start_date = datetime(2021, 1, 1)
        self.end_date = datetime(2022, 12, 31)

    def test_happy_flow(self):
        with GitLogFactory((self.git_log_entry1, self.git_log_entry2)):
            git = GitClient("/tmp")
            git_log = git.log(
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
            )
            logs = [x for x in git_log]
        assert logs[0] == self.git_log_entry1
        assert logs[1] == self.git_log_entry2

    def test_no_email(self):
        git_log_entry = GitLogEntry(
            hash="2fdffa2",
            date="2020-02-10",
            email="-",
            summary="NEW Enable CORS for qa.mierecensioni.it (HEAD -> master, origin/master)",
        )
        with GitLogFactory((git_log_entry,)):
            git = GitClient("/tmp")
            git_log = git.log(
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
            )
            logs = [x for x in git_log]
        assert logs[0] == git_log_entry

    def test_no_commits(self):
        with GitLogFactory(tuple()):
            git = GitClient("/tmp")
            git_log = git.log(
                branch="master",
                start_date=self.start_date,
                end_date=self.end_date,
                author="john",
            )
            logs = [x for x in git_log]
        assert not logs

    def test_start_date_string(self):
        with GitLogFactory(tuple()), pytest.raises(NotADate):
            git = GitClient("/tmp")
            git_log = git.log(
                branch="master",
                start_date="XXX",
                end_date=self.end_date,
                author="john",
            )
            [x for x in git_log]

    def test_end_date_string(self):
        with GitLogFactory(tuple()), pytest.raises(NotADate):
            git = GitClient("/tmp")
            git_log = git.log(
                branch="master",
                start_date=self.start_date,
                end_date="XXX",
                author="john",
            )
            [x for x in git_log]


class TestDiff:
    def setup(self):
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

    def test_happy_flow(self):
        with GitDiffFactory((self.git_diff_entry1, self.git_diff_entry2)):
            git = GitClient("/tmp")
            git_log = git.diff(hash="2fdffa2")
            diffs = [x for x in git_log]
        assert diffs[0] == self.git_diff_entry1
        assert diffs[1] == self.git_diff_entry2

    def test_no_insertions(self):
        git_diff_entry = GitDiffEntry(
            insertions="-",
            deletions="2",
            path="/tmp1",
        )
        with GitDiffFactory((git_diff_entry,)):
            git = GitClient("/tmp")
            git_log = git.diff(hash="2fdffa2")
            diffs = [x for x in git_log]
        assert diffs[0] == git_diff_entry

    def test_no_deletions(self):
        git_diff_entry = GitDiffEntry(
            insertions="10",
            deletions="-",
            path="/tmp1",
        )
        with GitDiffFactory((git_diff_entry,)):
            git = GitClient("/tmp")
            git_log = git.diff(hash="2fdffa2")
            diffs = [x for x in git_log]
        assert diffs[0] == git_diff_entry
