from pathlib import Path

from dynaconf import Dynaconf

conf_dir = Path(__file__).parent.resolve()

settings = Dynaconf(
    envvar_prefix="GIT_LOC",
    settings_files=[
        conf_dir / "settings_default.toml",
        conf_dir / "settings_development.toml",
        conf_dir / "settings_test.toml",
        conf_dir / ".secrets.toml",
    ],
    environments=True,
)
