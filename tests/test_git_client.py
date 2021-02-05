from git_loc.git_client import GitClient

from .testfactories.git_log_factory import (
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

    def test_happy_flow(self):
        git = GitClient("/tmp")
        git_log = git.log(
            branch="master",
            from_date="2021-01-01",
            to_date="2022-12-31",
            author="foo",
        )
        with GitLogFactory((self.git_log_entry1, self.git_log_entry2)):
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
        git = GitClient("/tmp")
        git_log = git.log(
            branch="master",
            from_date="2021-01-01",
            to_date="2022-12-31",
            author="foo",
        )
        with GitLogFactory((git_log_entry,)):
            logs = [x for x in git_log]
        assert logs[0] == git_log_entry

    def test_no_commits(self):
        git = GitClient("/tmp")
        git_log = git.log(
            branch="master",
            from_date="2021-01-01",
            to_date="2022-12-31",
            author="foo",
        )
        with GitLogFactory(tuple()):
            logs = [x for x in git_log]
        assert not logs


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
        git = GitClient("/tmp")
        git_log = git.diff(hash="2fdffa2")
        with GitDiffFactory((self.git_diff_entry1, self.git_diff_entry2)):
            diffs = [x for x in git_log]
        assert diffs[0] == self.git_diff_entry1
        assert diffs[1] == self.git_diff_entry2

    def test_no_insertions(self):
        git_diff_entry = GitDiffEntry(
            insertions="-",
            deletions="2",
            path="/tmp1",
        )
        git = GitClient("/tmp")
        git_log = git.diff(hash="2fdffa2")
        with GitDiffFactory((git_diff_entry,)):
            diffs = [x for x in git_log]
        assert diffs[0] == git_diff_entry

    def test_no_deletions(self):
        git_diff_entry = GitDiffEntry(
            insertions="10",
            deletions="-",
            path="/tmp1",
        )
        git = GitClient("/tmp")
        git_log = git.diff(hash="2fdffa2")
        with GitDiffFactory((git_diff_entry,)):
            diffs = [x for x in git_log]
        assert diffs[0] == git_diff_entry
