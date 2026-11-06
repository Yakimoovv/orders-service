# orders-service

A command-line tool for managing orders of a pen-plotter service that writes handwritten lecture notes and homework. Built with Python 3.13, tested with pytest, typed with mypy.

Orders are stored in a local SQLite database. The tool can add orders, change their status, delete them, list and filter them, show statistics, export orders to a CSV table for Excel, and migrate old orders from a JSON file.

## Features

- Add an order: customer, work type, number of pages, deadline, rate per page; each order gets a unique number
- Change an order's status or delete an order by its number
- Mark an order as urgent (price × 1.5)
- List orders, filter by status, urgency or overdue deadline, see the total price
- Show statistics: number of orders, revenue, urgent orders, orders by type
- Export orders to CSV (opens correctly in Excel, including Russian text), optionally filtered by status
- Migrate orders from the old JSON format into the database in one transaction: all or nothing
- `--verbose` mode logs how long each command took
- Input validation with clear error messages
- Safe storage: every change is a database transaction, CSV exports are written atomically, and a file that isn't a database is never overwritten

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

By default, orders are stored in the SQLite database `orders.db` in the current folder.
Use `--file` to choose another file. It goes **before** the command.

`add` and `migrate` create the database if it doesn't exist yet. All other commands require an existing database, so a typo in `--file` gives a "file not found" error instead of silently creating an empty database.

### Add an order

```bash
orders add <customer> <work_type> <pages> <deadline> <rate> [--urgent]
```

`deadline` is a date in `YYYY-MM-DD` format and can't be in the past.

`work_type` is one of: `notes`, `homework`, `report`.

The command prints the number of the new order, for example `Добавлен заказ №3: ...`. Use this number with `status` and `delete`.

```bash
orders add Anton notes 20 2027-03-01 50
orders add Maria report 12 2027-03-10 80 --urgent
orders --file my_orders.db add Ivan homework 8 2027-03-15 60
```

### List orders

```bash
orders list                  # all orders
orders list --status new     # only orders with status "new"
orders list --urgent         # only urgent orders
orders list --overdue        # only overdue orders (deadline passed, not done/cancelled)
```

### Change status

```bash
orders status <id> <new_status>
```

`new_status` is one of: `new`, `in_progress`, `done`, `cancelled`.

```bash
orders status 3 done
```

### Delete an order

```bash
orders delete <id>
```

```bash
orders delete 3
```

If there is no order with this number, both commands print an error and exit with code 1.

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
The `№` column contains the order number from the database.
Exporting into the orders file itself is refused, so the database can't be overwritten by mistake.

### Migrate from JSON

Earlier versions stored orders in a JSON file. To move them into the database:

```bash
orders migrate orders.json
```

All orders are added in a single transaction: if any of them fails, none are added.
Migration is refused if the database already contains orders, so running it twice can't create duplicates.

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
| 1 | Data error (file not found, not a database, invalid order, order not found, migration into a non-empty database) |
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

Run all checks at once (stops at the first failure):

```bash
./scripts/check.sh
```

## Project structure

```text
orders/
  models.py      # Order class: validation, price, dict conversion
  repository.py  # SqliteOrderRepository: orders table, add/get/list/set_status/delete, transactions
  storage.py     # OrderBook: statistics; JSON load/save used by migrate
  exceptions.py  # error hierarchy: OrderError, ValidationError, StorageError
  cli.py         # command-line interface (argparse)
  export.py      # CSV rows generator
  timing.py      # @timed decorator: logs command execution time
  atomic.py      # AtomicWriter context manager: safe file writes
  __main__.py    # entry point for python -m orders
tests/           # pytest tests
scripts/
  check.sh       # runs ruff, mypy and pytest in one go
```
