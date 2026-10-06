# orders-service

A command-line tool for managing orders of a pen-plotter service that writes lecture notes and homework by hand.

Orders are stored in a local JSON file. The tool can add orders, list and filter them, and show statistics.

## Features

- Add an order: customer, work type, number of pages, deadline, rate per page
- Mark an order as urgent (price × 1.5)
- List orders, filter by status or urgency, see the total price
- Show statistics: number of orders, revenue, urgent orders, orders by type
- Input validation with clear error messages
- Safe saving: the data file is written atomically, and a corrupted file is never overwritten

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

`work_type` is one of: `notes`, `homework`, `report`.

```bash
orders add Anton notes 20 2026-11-01 50
orders add Maria report 12 2026-10-20 80 --urgent
orders --file my_orders.json add Ivan homework 8 2026-10-15 60
```

### List orders

```bash
orders list                  # all orders
orders list --status new     # only orders with status "new"
orders list --urgent         # only urgent orders
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

## Project structure

```text
orders/
  models.py      # Order class: validation, price, JSON conversion
  storage.py     # OrderBook: list of orders, save/load, statistics
  exceptions.py  # error hierarchy: OrderError, ValidationError, StorageError
  cli.py         # command-line interface (argparse)
  __main__.py    # entry point for python -m orders
tests/           # pytest tests
```
