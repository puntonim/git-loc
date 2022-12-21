git-loc
=======

Count the lines of code (LOC) modified in a Git repo branch in all the non-merge 
 commits, authored by an author, within a start and end date, and ignoring some files.

Tested with git version 2.23.0 and Python 3.

If the git binary cannot be found, then edit the settings `GIT_LOG_BIN` and 
 `GIT_DIFF_BIN` in `git_loc/conf/settings_default.py` (or better in `git_loc/conf/.secrets.toml`).


Usage
=====
```shell
$ poetry run git-loc count
```

To use CLI params, instead of typing them intractively:
```shell
$ poetry run git-loc count \
   --dir /tmp/mierecensioni-be \
   --branch master \
   --start-date 2020-01-01 \
   --end-date 2020-12-31 \
   --author puntonim \
   --ignore-file .gitignore \
   --ignore-file package-lock.json \
   --ignore-file poetry.lock \
   --ignore-file cassettes
```


Example
-------
```shell
$ poetry run git-loc count

Git root dir: /tmp/mierecensioni-be
Git branch: master
Commits author name or email [not required]: puntonim
Commits start date (eg.: 2020-01-12) [not required]: 2020-01-01
Commits end date (eg.: 2020-01-12) [not required]: 2020-12-31
File names to ignore (use ; as separator) [not required]: .gitignore;package-lock.json;poetry.lock;cassettes

Computing...
                                   Files
┏━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ insertions ┃ deletions ┃ file path                                       ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1          │ 1         │ www/templates/www/new_survey.html               │
│ 69         │ 23        │ core/indexer.py                                 │
│ 6          │ 2         │ core/signals.py                                 │
│ 4          │ 1         │ core/indexer.py                                 │
│ 9          │ 7         │ scripts/fixture_studio_bonacina.py              │
│ 1224       │ 0         │ scripts/fixture_studio_bonacina.py              │
│ 64         │ 18        │ scripts/fixture_sample_data2.py                 │
│ 0          │ 1         │ api/urls.py                                     │
│ 0          │ 5         │ api/views.py                                    │
│ 0          │ 1         │ core/admin.py                                   │
│ 16         │ 0         │ core/migrations/0004_delete_site.py             │
│ 1          │ 5         │ core/models.py                                  │
│ 0          │ 1         │ scripts/fixture_admin_user.py                   │
│ 0          │ 8         │ scripts/fixture_sample_data1.py                 │
│ 0          │ 14        │ tests/api/views/test_terms_views.py             │
│ 0          │ 13        │ tests/factories/models_factories.py             │
│ 4          │ 1         │ core/signals.py                                 │
│ 1          │ 1         │ scripts/fixture_sample_data1.py                 │
│ 1          │ 1         │ scripts/fixture_sample_data2.py                 │
│ 16         │ 12        │ conf/locale/it/LC_MESSAGES/django.po            │
│ 34         │ 0         │ www/forms.py                                    │
│ 6          │ 0         │ www/static/www/css/base_navbar.css              │
│ 15         │ 0         │ www/static/www/css/change_password.css          │
│ 25         │ 0         │ www/static/www/css/me.css                       │
│ 1          │ 1         │ www/templates/www/base_navbar.html              │
│ 58         │ 0         │ www/templates/www/change_password.html          │
│ 43         │ 0         │ www/templates/www/me.html                       │
│ 1          │ 1         │ www/templates/www/new_survey.html               │
│ 1          │ 1         │ www/templates/www/patients.html                 │
│ 1          │ 2         │ www/templates/www/redemption_code_search.html   │
│ 1          │ 1         │ www/templates/www/surveys.html                  │
│ 6          │ 0         │ www/urls.py                                     │
│ 47         │ 0         │ www/views.py                                    │
│ 10         │ 6         │ conf/locale/it/LC_MESSAGES/django.po            │
│ 2          │ 1         │ core/validators.py                              │
│ 5          │ 7         │ scripts/fixture_sample_data1.py                 │
│ 5          │ 4         │ scripts/fixture_sample_data2.py                 │
│ 33         │ 18        │ www/forms.py                                    │
│ 5          │ 2         │ www/templates/www/new_survey.html               │
│ 202        │ 17        │ scripts/fixture_sample_data1.py                 │
│ 141        │ 2         │ scripts/fixture_sample_data2.py                 │
│ 4          │ 6         │ scripts/index_sample_data.py                    │
│ 1          │ 1         │ api/domain/domain_models.py                     │
│ 1          │ 1         │ core/validators.py                              │
│ 45         │ 97        │ scripts/fixture_sample_data1.py                 │
│ 34         │ 79        │ scripts/fixture_sample_data2.py                 │
│ 1          │ 3         │ www/views.py                                    │
│ 2          │ 2         │ utils/metrics.py                                │
│ 9          │ 0         │ api/domain/domain_models.py                     │
│ 19         │ 0         │ www/views.py                                    │
│ 5          │ 0         │ api/apps.py                                     │
│ 8          │ 0         │ api/views.py                                    │
│ 10         │ 0         │ conf/docker-elk/es-index-template-mappings.json │
│ 10         │ 1         │ conf/settings_base.py                           │
│ 6          │ 0         │ conf/settings_development_TEMPLATE.py           │
│ 2          │ 1         │ conf/settings_production_TEMPLATE.py            │
│ 3          │ 0         │ conf/settings_runtest.py                        │
│ 3          │ 3         │ core/managers.py                                │
│ 3          │ 2         │ core/signals.py                                 │
│ 2          │ 0         │ requirements/requirements_base.txt              │
│ 6          │ 1         │ tests/conftest.py                               │
│ 3          │ 3         │ tests/factories/models_factories.py             │
│ 41         │ 0         │ utils/metrics.py                                │
│ 7          │ 0         │ utils/network.py                                │
│ 0          │ 9         │ core/utils.py => utils/random.py                │
│ 6          │ 0         │ conf/settings_base.py                           │
│ 6          │ 15        │ conf/settings_development_TEMPLATE.py           │
│ 4          │ 13        │ conf/settings_production_TEMPLATE.py            │
│ 5          │ 0         │ core/apps.py                                    │
│ 0          │ 0         │ utils/__init__.py                               │
│ 17         │ 0         │ utils/sentry.py                                 │
│ 4          │ 3         │ api/views.py                                    │
│ 1          │ 1         │ conf/postactivate_TEMPLATE                      │
│ 14         │ 0         │ conf/settings_development_TEMPLATE.py           │
│ 13         │ 0         │ conf/settings_production_TEMPLATE.py            │
│ 1          │ 0         │ requirements/requirements_base.txt              │
│ 5          │ 0         │ README.md                                       │
│ 2          │ 2         │ Makefile                                        │
│ 1          │ 0         │ conf/settings_base.py                           │
│ 1          │ 1         │ conf/{settings_test.py => settings_runtest.py}  │
│ 1          │ 1         │ tests/conftest.py                               │
│ ignored    │ ignored   │ .gitignore                                      │
│ 0          │ 881       │ conf/fail2ban-jail.local                        │
│ 0          │ 38        │ conf/iptables-rules                             │
│ 0          │ 12        │ conf/knockd.conf                                │
│ 0          │ 120       │ conf/nginx.conf                                 │
│ 0          │ 48        │ conf/uwsgi.ini                                  │
│ 0          │ 19        │ conf/uwsgi_params                               │
└────────────┴───────────┴─────────────────────────────────────────────────┘

Repo root dir: /tmp/mierecensioni-be
Branch: master
Author: puntonim
Start date: 2020-01-01
End date: 2020-12-31
Ignored files: ('.gitignore', 'package-lock.json', 'poetry.lock', 'cassettes')
LOC: 3905

```


Strategy
========
The strategy used to compute the LOC is the following:
- list all non-merge commits in the git repo branch, between the start date and the
   end date and with the given author
- for each commit, execute a git diff with the previous commit
- for each file in the diff, if the path does not match any files to be ignored, then
   add its additions and deletions (deletions as absolute integer).

The same strategy done with git commands would be:
```shell
$ git log master \
   --pretty=format:"%h %ad %ae %s%d" \
   --date=short \
   --no-merges \
   --since="2020-01-01" \
   --before="2020-01-05" \
   --author="puntonim"
4256921 2020-01-04 puntonim@gmail.com OPT Update copyright
2fdffa2 2020-01-04 puntonim@gmail.com NEW Enable CORS for qa.mierecensioni.it

$ git diff --numstat 4256921~1 4256921
5       0       README.md

$ git diff --numstat 2fdffa2~1 2fdffa2
2       2       Makefile
1       0       conf/settings_base.py
1       1       conf/{settings_test.py => settings_runtest.py}
3       10      .gitignore
1       1       tests/conftest.py
```
LOC is computed adding all the numbers reported by the git diff commands, but
 ignoring `.gitignore`, so: 14.


Development
===========

Tested with git version 2.23.0 and Python 3.11.

If the git binary cannot be found, then edit the settings `GIT_LOG_BIN` and 
 `GIT_DIFF_BIN` in `git_loc/conf/settings_default.py` (or better in `git_loc/conf/.secrets.toml`).

1 - System requirements
-----------------------

**Python 3.11**\
The target Python 3.11, install it with pyenv:
```sh
$ pyenv install -l  # List all available versions.
$ pyenv install 3.11.0
```

**Poetry**\
Pipenv is used to manage requirements (and virtual environments).\
Read more about Poetry [here](https://python-poetry.org/). \
Follow the [install instructions](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions).

**Pre-commit**\
Pre-commit is used to format the code with black before each git commit:
```sh
$ pip install --user pre-commit
# On macOS you can also:
$ brew install pre-commit
```

2 - Virtual environment and requirements
----------------------------------------

Create a virtual environment and install all deps with one Make command:
```sh
$ make poetry-create-env
# Or to recreate:
$ make poetry-destroy-and-recreate-env
```

Without using Makefile the full process is:
```sh
# Activate the Python version for the current project:
$ pyenv local 3.11.0  # It creates `.python-version`, to be git-ignored.
$ pyenv which python
~/.pyenv/versions/3.11.0/bin/python

# Now create a venv with poetry:
$ poetry env use ~/.pyenv/versions/3.11.0/bin/python
# Now you can open a shell and/or install:
$ poetry shell
# And finally, install all requirements:
$ poetry install
```

To add a new requirement:
```sh
$ poetry add requests
$ poetry add pytest --dev  # Dev only.
$ poetry add requests[security,socks]  # With extras.
```

3 - Pre-commit
--------------

```sh
$ pre-commit install
```

4 - Settings
------------

Copy [.secrets.EXAMPLE.toml](./git_loc/conf/.secrets.EXAMPLE.toml) to `.secrets.toml`
and fill it in with your values.
```sh
$ cp git_loc/conf/.secrets.EXAMPLE.toml git_loc/conf/.secrets.toml
```
In development, `dynaconf` loads the entries in this
file to override the default ones.

In production define environment variables with the prefix `GIT_LOC_`.


Testing
=======

Tests are compatible with `pytest` and non-compatible with `unittest.TestCase`.\
Run test with:
```sh
$ make test
$ pytest -s tests  # Alternative.
```
