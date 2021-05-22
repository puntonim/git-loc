This project is configured using setting files, managed by [dynaconf](https://github.com/rochacbruno/dynaconf).

# Settings files

Settings files are read in the following order:
- `settings_default.toml`
- `settings_development.toml`
- `settings_test.toml`

and the keys in the latter files override the keys in the previous files.

## Settings per environment

This project leverages Dynaconf's environments, but split into different files.
- PRODUCTION: use Dynaconf env `[default]` in `settings_default.toml`.
- DEVELOPMENT: use Dynaconf env `[default]` in `settings_development.toml`. With
   git untracked overrides in `secrets.toml` (not just for secrets).
- TEST: use Dynaconf env `[test]` in `settings_test.toml`.

Notice that different Dynaconf envs can be use din the same file, but this is not
the convention used in this file.

Notice that `settings_test.toml` only contains the environment `[test]` and is considered
only when running tests with `pytest` (this is configured in `conftest.py`).


# Secrets

Secrets are stored in:
- PRODUCTION: environment variables.
- DEVELOPMENT and TEST: in `./conf/secrets.toml` which is git-ignored (copy the example
   from `./conf/secrets.EXAMPLE.toml`)


# No `*.local.*` files

Dynaconf supports `*.local.*` files, eg. `settings_default.local.toml` would override
`settings_default.toml`. However, there is a problem: `settings_default.local.toml` would
also override `settings_test.toml` (and `settings_test.local.toml`) thus making it
impossible to have a separate file for the test environment.


# Settings vs constants

Notice that *settings* and *constants* are different concepts.

*Settings* are environment-specific configuration, eg:
 - urls to an external service in its production or test environment
 - secrets 
 - any configuration that is likely to be overridden in tests 
 - feature toggles

*Constants* have a fixed value that do not depend on the environment, eg:
 - KB = 1024
