import argparse
import csv
import logging
import sys
from datetime import date
from pathlib import Path

from orders.atomic import AtomicWriter
from orders.exceptions import (
    OrderError,
    StorageError,
    StorageNotFoundError,
    ValidationError,
)
from orders.export import order_rows
from orders.models import WORK_TYPES, Order, Status
from orders.repository import SqliteOrderRepository
from orders.storage import OrderBook
from orders.timing import timed


def _open_repo(path: Path, must_exist: bool) -> SqliteOrderRepository:
    if must_exist and not path.exists():
        raise StorageNotFoundError(f"Файл не найден: {path}")
    return SqliteOrderRepository(path)


@timed
def cmd_list(args: argparse.Namespace) -> int:
    path = args.file
    try:
        with _open_repo(path, must_exist=True) as repo:
            orders = repo.list(args.status)
    except StorageError as e:
        print(e, file=sys.stderr)
        return 1

    if args.urgent:
        urgent_book = [order for order in orders if order.urgent]
        orders = urgent_book
    if args.overdue:
        today = date.today()
        orders = [order for order in orders if order.is_overdue(today)]
    if len(orders) == 0:
        print("Заказов нет")
        return 0
    total = 0
    for order in orders:
        total += order.price()
        print(order)
    print(f"Итоговая сумма {total}, всего заказов {len(orders)}")
    return 0


@timed
def cmd_add(args: argparse.Namespace) -> int:
    path = args.file
    try:
        if args.deadline < date.today():
            raise ValidationError("deadline", "дата в прошлом")
        order = Order(
            args.customer,
            args.work_type,
            args.pages,
            args.deadline,
            args.rate,
            urgent=args.urgent,
        )
    except OrderError as e:
        print(e, file=sys.stderr)
        return 1

    try:
        with _open_repo(path, must_exist=False) as repo:
            order_id = repo.add(order)
    except StorageError as e:
        print(e, file=sys.stderr)
        return 1
    print(f"Добавлен заказ №{order_id}: {order}")
    return 0


@timed
def cmd_stats(args: argparse.Namespace) -> int:
    path = args.file
    try:
        with _open_repo(path, must_exist=True) as repo:
            orders = repo.list()
    except StorageError as e:
        print(e, file=sys.stderr)
        return 1
    book = OrderBook("Глеб", orders)
    stats = book.stats()
    print(f"Всего заказов: {stats.total_orders}")
    print(f"Выручка: {stats.total_revenue}")
    print(f"Срочных: {stats.urgent_count}")
    print(f"Типы: {stats.by_type}")
    return 0


@timed
def cmd_export(args: argparse.Namespace) -> int:
    path = args.file
    if path.resolve() == args.path.resolve():
        print("Путь к файлу базы данных и csv одинаковые", file=sys.stderr)
        return 1
    try:
        with _open_repo(path, must_exist=True) as repo:
            orders = repo.list(args.status)
    except StorageError as e:
        print(e, file=sys.stderr)
        return 1
    with AtomicWriter(args.path, encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(order_rows(orders))
    print(f"Экспортировано {len(orders)} заказов")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=Path, default=Path("orders.db"), help="Путь к файлу заказов"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Показать время выполнения команды"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="Список заказов")
    list_parser.add_argument(
        "--status", type=Status, choices=list(Status), default=None, help="По статусу"
    )
    list_parser.add_argument("--urgent", action="store_true", help="Только срочные")
    list_parser.add_argument(
        "--overdue", action="store_true", help="Только просроченные"
    )

    add_parser = subparsers.add_parser("add", help="Добавить заказ")
    add_parser.add_argument("customer")
    add_parser.add_argument("work_type", choices=WORK_TYPES)
    add_parser.add_argument("pages", type=int)
    add_parser.add_argument("deadline", type=date.fromisoformat)
    add_parser.add_argument("rate", type=int)
    add_parser.add_argument("--urgent", action="store_true")

    subparsers.add_parser("stats", help="Статистика по заказам")

    export_parser = subparsers.add_parser("export", help="Выгрузить заказы в таблицу")
    export_parser.add_argument(
        "path",
        type=Path,
        help="Путь к файлу с таблицей с заказами",
    )
    export_parser.add_argument(
        "--status", type=Status, choices=list(Status), default=None, help="По статусу"
    )

    args = parser.parse_args(argv)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.command == "list":
        return cmd_list(args)
    elif args.command == "add":
        return cmd_add(args)
    elif args.command == "stats":
        return cmd_stats(args)
    elif args.command == "export":
        return cmd_export(args)
    return 1
