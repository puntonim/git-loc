import click

from .__version__ import __version__
from .views import introspection, main


# The entrypoint.
# Run in dev with: `$ poetry run git-loc`.
# Run in prod (after a pip install) with: `$ git-loc`.
@click.group(help="Count LOC in a Git repo branch")
@click.version_option(__version__)
def cli() -> None:
    pass


# Register all sub-commands.
cli.add_command(introspection._health)
cli.add_command(introspection._unhealth)
cli.add_command(introspection._settings)
cli.add_command(main._count)
