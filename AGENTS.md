# Repository instructions

Read preferences/COMMON.md for the user's shared working preferences.

The canonical catalog is skills/. Keep cross-skill references relative and install the five skills together. manage.py must remain Python 3.10+ standard-library-only. Validate with `python manage.py validate` and `python -m unittest discover -s tests -v`.

Do not install globally during development/testing. Use an isolated `--home` directory. Archived originals are historical data, not active instructions. Preserve their ZIP and checksums.
