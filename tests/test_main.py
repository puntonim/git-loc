import pytest

from git_loc.main import AuthorMismatch, FromDateMismatch, LocCounter, ToDateMismatch

from .testfactories.git_log_factory import (
    GitDiffEntry,
    GitDiffFactory,
    GitLogEntry,
    GitLogFactory,
)


class TestLocCounter:
    def setup(self):
        self.git_log_entry1 = GitLogEntry(
            hash="1111111",
            date="2020-02-10",
            email="foo@gmail.com",
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

    def test_happy_flow(self):
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            loc_tot = counter.count(
                branch="master",
                from_date="2020-02-01",
                to_date="2020-03-01",
                author="foo",
                # files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 26

    def test_two_commits(self):
        git_log_entry2 = GitLogEntry(
            hash="2222222",
            date="2020-02-11",
            email="foo@gmail.com",
            summary="NEW Answer model",
        )
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1, git_log_entry2)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            loc_tot = counter.count(
                branch="master",
                from_date="2020-02-01",
                to_date="2020-03-01",
                author="foo",
                # files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 52

    def test_no_insertions(self):
        git_diff_entry3 = GitDiffEntry(
            insertions="-",
            deletions="1",
            path="/tmp1",
        )
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2, git_diff_entry3)
        ):
            loc_tot = counter.count(
                branch="master",
                from_date="2020-02-01",
                to_date="2020-03-01",
                author="foo",
                # files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 27

    def test_no_deletions(self):
        git_diff_entry3 = GitDiffEntry(
            insertions="1",
            deletions="-",
            path="/tmp1",
        )
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2, git_diff_entry3)
        ):
            loc_tot = counter.count(
                branch="master",
                from_date="2020-02-01",
                to_date="2020-03-01",
                author="foo",
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
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (
                self.git_diff_entry1,
                self.git_diff_entry2,
                git_diff_entry3,
                git_diff_entry4,
            )
        ):
            loc_tot = counter.count(
                branch="master",
                from_date="2020-02-01",
                to_date="2020-03-01",
                author="foo",
                files_to_ignore=("package-lock.json", ".gitignore"),
            )
        assert loc_tot == 26

    def test_author_mismatch(self):
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(AuthorMismatch):
                counter.count(
                    branch="master",
                    from_date="2020-02-01",
                    to_date="2020-03-01",
                    author="XXX",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )

    def test_from_date_mismatch(self):
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(FromDateMismatch):
                counter.count(
                    branch="master",
                    from_date="2021-02-01",
                    to_date="2021-03-01",
                    author="foo",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )

    def test_to_date_mismatch(self):
        counter = LocCounter(root_dir="/tmp")
        with GitLogFactory((self.git_log_entry1,)), GitDiffFactory(
            (self.git_diff_entry1, self.git_diff_entry2)
        ):
            with pytest.raises(ToDateMismatch):
                counter.count(
                    branch="master",
                    from_date="2020-02-01",
                    to_date="2020-02-01",
                    author="foo",
                    # files_to_ignore=("package-lock.json", ".gitignore"),
                )
