from typing import Collection, Optional

from git_loc.clients.git_client import GitDiffEntry, GitLogEntry

from ..testutils.settings_testutils import override_settings


# Notice that this is a context manager!
class GitLogFactory:
    def __init__(self, git_log_entries: Optional[Collection[GitLogEntry]]):
        self.mocks = list()
        self.git_log_entries = git_log_entries

    def __enter__(self):
        def_args = '/bin/echo "" ; /usr/bin/true'
        if self.git_log_entries is not None:
            def_args = '/bin/echo "'
            for git_log_entry in self.git_log_entries:
                def_args += f"'{git_log_entry.hash} {git_log_entry.date} {git_log_entry.email} {git_log_entry.summary}'\n"
            def_args += '" ; /usr/bin/true'

        self.override_settings = override_settings(
            GIT_LOG_BIN=def_args, DO_USE_POPEN_SHELL=True, do_allow_new_settings=True
        )
        self.override_settings.__enter__()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.override_settings.__exit__()


# Notice that this is a context manager!
class GitDiffFactory:
    def __init__(self, git_diff_entries: Optional[Collection[GitDiffEntry]]):
        self.mocks = list()
        self.git_diff_entries = git_diff_entries

    def __enter__(self):
        def_args = '/bin/echo "" ; /usr/bin/true'
        if self.git_diff_entries is not None:
            def_args = '/bin/echo "'
            for git_diff_entry in self.git_diff_entries:
                def_args += f"{git_diff_entry.insertions}\t{git_diff_entry.deletions}\t{git_diff_entry.path}\n"
            def_args += '" ; /usr/bin/true'

        self.override_settings = override_settings(
            GIT_DIFF_BIN=def_args, DO_USE_POPEN_SHELL=True, do_allow_new_settings=True
        )
        self.override_settings.__enter__()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.override_settings.__exit__()
