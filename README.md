# SmartATM

SmartATM is a Python ATM simulation app with:

- account creation and login
- deposits and withdrawals
- balance checks
- transaction history
- CLI and Tkinter GUI interfaces

## Requirements

- Python 3.10+ (3.12 recommended)
- `tkinter` installed (for GUI mode)

## Project Setup

From your parent directory (the folder that contains `smart/`):

```bash
cd /path/to/parent
python3 -m venv smart/.venv
source smart/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r smart/requirements.txt
```

## Run the App

Run from the parent directory:

```bash
python -m smart
```

Mode options:

```bash
python -m smart --cli
python -m smart --gui
python -m smart --version
```

## Data Storage

Account data is stored in JSON format and created automatically on first run.

## Development

Optional checks:

```bash
pytest
flake8 .
black .
```
