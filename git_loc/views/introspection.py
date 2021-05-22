from datetime import datetime

import click

from ..conf import settings as conf_settings
from ..utils import command, printer


@click.command(cls=command.BaseCommand, name="health")
def _health() -> None:
    """
    Test command to print the timestamp and logs.
    """
    return health()


def health() -> None:
    now = datetime.now().astimezone().isoformat()
    console = printer.ConsoleAdapter()
    console.print(now)


@click.command(cls=command.BaseCommand, name="unhealth")
def _unhealth() -> None:
    """
    Raise a test exception.
    """
    return unhealth()


def unhealth() -> None:
    now = datetime.now().astimezone().isoformat()
    raise UnhealthCommandException(ts=now)


class UnhealthCommandException(Exception):
    def __init__(self, ts: str):
        self.ts = ts


@click.command(cls=command.BaseCommand, name="settings")
def _settings() -> None:
    """
    Print the settings.
    """
    return settings()


def settings() -> None:
    console = printer.ConsoleAdapter()
    for key, value in conf_settings.as_dict().items():
        if isinstance(value, str) and (
            "SECRET" in key.upper() or "PASS" in key.upper() or "TOKEN" in key.upper()
        ):
            value = value[:3] + "**REDACTED**"
        console.print(f"{key} = {value}")
