# orders-service

A command-line tool for managing orders of a pen-plotter service that writes handwritten lecture notes and homework. Built with Python 3.13, tested with pytest, typed with mypy.

Orders are stored in a local JSON file that is always written atomically. The tool can add orders, list and filter them by status or urgency, show statistics, and export orders to a CSV table for Excel.

## Features

- Add an order: customer, work type, number of pages, deadline, rate per page
- Mark an order as urgent (price × 1.5)
- List orders, filter by status, urgency or overdue deadline, see the total price
- Show statistics: number of orders, revenue, urgent orders, orders by type
- Export orders to CSV (opens correctly in Excel, including Russian text), optionally filtered by status
- `--verbose` mode logs how long each command took
- Input validation with clear error messages
- Safe saving: the data file and CSV exports are written atomically, and a corrupted file is never overwritten

## Requirements

- Python 3.13+

## Installation

Clone the repository:

```bash
git clone https://github.com/Yakimoovv/orders-service.git
cd orders-service
```

Create and activate a virtual environment.

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project. `[dev]` also installs tools for testing and linting:

```bash
pip install -e ".[dev]"
```

Check that it works:

```bash
orders --help
```

## Usage

By default, orders are stored in `orders.json` in the current folder.
Use `--file` to choose another file. It goes **before** the command.

### Add an order

```bash
orders add <customer> <work_type> <pages> <deadline> <rate> [--urgent]
```

`deadline` is a date in `YYYY-MM-DD` format and can't be in the past.

`work_type` is one of: `notes`, `homework`, `report`.

```bash
orders add Anton notes 20 2027-03-01 50
orders add Maria report 12 2027-03-10 80 --urgent
orders --file my_orders.json add Ivan homework 8 2027-03-15 60
```

### List orders

```bash
orders list                  # all orders
orders list --status new     # only orders with status "new"
orders list --urgent         # only urgent orders
orders list --overdue        # only overdue orders (deadline passed, not done/cancelled)
```

### Show statistics

```bash
orders stats
```

Example output (the CLI output is in Russian):

```text
Всего заказов: 3
Выручка: 2920
Срочных: 1
Типы: {'notes': 1, 'report': 1, 'homework': 1}
```

### Export to CSV

```bash
orders export <path> [--status STATUS]
```

```bash
orders export orders.csv                 # all orders
orders export done.csv --status done     # only finished orders
```

The file uses `;` as the delimiter and UTF-8 with BOM, so Excel opens it with columns and correct Cyrillic text.
Exporting into the orders file itself is refused, so the data file can't be overwritten by mistake.

### Verbose mode

`--verbose` goes **before** the command, like `--file`. Each command then logs its execution time to stderr:

```bash
orders --verbose list
```

```text
...
DEBUG:orders.timing:Функция cmd_list заняла 0.002 с
```

### Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | Data error (file not found, corrupted file, invalid order) |
| 2 | Invalid command-line arguments |

Errors are printed to stderr.

## Development

Run tests:

```bash
pytest
```

Type check:

```bash
mypy orders
```

Lint and format check:

```bash
ruff check .
ruff format --check .
```

Run all checks at once: `ruff check . ; mypy orders ; pytest`

## Project structure

```text
orders/
  models.py      # Order class: validation, price, JSON conversion
  storage.py     # OrderBook: list of orders, save/load, statistics
  exceptions.py  # error hierarchy: OrderError, ValidationError, StorageError
  cli.py         # command-line interface (argparse)
  export.py      # CSV rows generator
  timing.py      # @timed decorator: logs command execution time
  atomic.py      # AtomicWriter context manager: safe file writes
  __main__.py    # entry point for python -m orders
tests/           # pytest tests
```
