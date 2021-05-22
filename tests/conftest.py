import pytest
from click.testing import CliRunner

from git_loc.conf import settings


def pytest_configure(config):
    """
    Set the `test` environment in dynaconf such that the settings in `settings_test.toml`
    are being used (in the section [test]).
    And configure the marker pytest.mark.novcr.
    """
    settings.configure(FORCE_ENV_FOR_DYNACONF="test")
    # Ensure that the test settings are used.
    if not settings.IS_TEST:
        raise RuntimeError("Configuration error: you are NOT using the test settings")


@pytest.fixture(scope="session", autouse=True)
def assert_test_settings_are_used():
    """
    Ensure (a second time) that the test settings are used.
    """
    if not settings.IS_TEST:
        raise RuntimeError("Configuration error: you are NOT using the test settings")


@pytest.fixture(scope="session")
def monkeysession(request):
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(autouse=True, scope="function")
def cli_runner():
    return CliRunner(mix_stderr=False)
