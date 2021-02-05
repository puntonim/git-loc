git-loc
=======

Count the lines of code (LOC) modified in a Git repo branch in all the non-merge 
 commits, authored by an author, within a start and end date, and ignoring some files.

Tested with git version 2.23.0 and Python 3.

If the git binary cannot be found, then edit the var `GIT_LOG_BIN` in
 `git_loc/git_client.py`.


Usage
-----
```shell
$ python -m git_loc.main <REPO-ROOT-PATH*> <BRANCH*> <FROM-DATE> <TO-DATE> <AUTHOR> <IGNORE-FILES-LIST>
```
`*` means that the CLI arg is required.


Example
-------
```shell
$ python -m git_loc.main ~/workspace/mierecensioni-be master 2020-01-01 2020-12-31 puntonim .gitignore package-lock.json
www/templates/www/new_survey.html
	>>> Insertions #1 | Deletions #1

core/indexer.py
	>>> Insertions #69 | Deletions #23

core/signals.py
	>>> Insertions #6 | Deletions #2

core/indexer.py
	>>> Insertions #4 | Deletions #1

scripts/fixture_sample_data2.py
	>>> Insertions #64 | Deletions #18

api/urls.py
	>>> Insertions #0 | Deletions #1

api/views.py
	>>> Insertions #0 | Deletions #5

core/admin.py
	>>> Insertions #0 | Deletions #1

core/migrations/0004_delete_site.py
	>>> Insertions #16 | Deletions #0

tests/conftest.py
	>>> Insertions #1 | Deletions #1

.gitignore
	Ignoring

conf/fail2ban-jail.local
	>>> Insertions #0 | Deletions #881
...

TOTAL LOC: 3905
```


Strategy
--------
The strategy used to compute the LOC is the following:
- list all non-merge commits in the git repo branch, between the from_date and the
   to_date and with the given author
- for each commit, issue a git diff vs the previous commit
- for each file in the diff, if the path does not match the file to ignore list, then
   add its additions and deletions (deletions as absolute int).

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
-----------

Tested with git version 2.23.0 and Python 3.

If the git binary cannot be found, then edit the var `GIT_LOG_BIN` in
 `git_loc/git_client.py`.
 
There is no virtual environment.

To run tests, `pytest` is required:
```shell
$ pytest -s tests
```
