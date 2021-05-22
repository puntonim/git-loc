import re

from rich.console import Console

from ..conf import settings

ESCAPE_ANSI_REGEX = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class ConsoleAdapter(Console):
    def log(self, *args, **kwargs):
        if not settings.DO_SUPPRESS_PRINT:
            super().log(*args, **kwargs)

    def print(self, *args, **kwargs):
        if not settings.DO_SUPPRESS_PRINT:
            super().print(*args, **kwargs)

    def status(self, *args, **kwargs):
        if not settings.DO_SUPPRESS_PRINT:
            return super().status(*args, **kwargs)


def remove_ansi_chars(text):
    """
    Escape all ANSI chars from the given text.
    ANSI chars are typically added to produce colored output.
    """
    return ESCAPE_ANSI_REGEX.sub("", text)
