import argparse
import sys
from pathlib import Path

from orders.exceptions import (
    OrderError,
    StorageCorruptedError,
    StorageError,
    StorageNotFoundError,
)
from orders.models import WORK_TYPES, Order
from orders.storage import OrderBook


def cmd_list(args: argparse.Namespace) -> int:
    path = args.file
    try:
        book = OrderBook.load(path, "Глеб")
    except StorageError as e:
        print(e, file=sys.stderr)
        return 1

    orders = book.orders
    if args.status is not None:
        orders = book.by_status(args.status)
    if args.urgent:
        urgent_book = []
        for order in orders:
            if order.urgent:
                urgent_book.append(order)
        orders = urgent_book
    if len(orders) == 0:
        print("Заказов нет")
        return 0
    total = 0
    for order in orders:
        total += order.price()
        print(order)
    print(f"Итоговая сумма {total}, всего заказов {len(orders)}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    path = args.file
    try:
        book = OrderBook.load(path, "Глеб")
    except StorageNotFoundError:
        book = OrderBook("Глеб")
    except StorageCorruptedError as e:
        print(e, file=sys.stderr)
        return 1
    try:
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
    book.add(order)
    book.save(path)
    print(f"Добавлен: {order}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    path = args.file
    try:
        book = OrderBook.load(path, "Глеб")
    except StorageError as e:
        print(e, file=sys.stderr)
        return 1
    stats = book.stats()
    print(f"Всего заказов: {stats.total_orders}")
    print(f"Выручка: {stats.total_revenue}")
    print(f"Срочных: {stats.urgent_count}")
    print(f"Типы: {stats.by_type}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=Path, default=Path("orders.json"), help="Путь к файлу заказов"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="Список заказов")
    list_parser.add_argument("--status", default=None, help="По статусу")
    list_parser.add_argument("--urgent", action="store_true", help="Только срочные")

    add_parser = subparsers.add_parser("add", help="Добавить заказ")
    add_parser.add_argument("customer")
    add_parser.add_argument("work_type", choices=WORK_TYPES)
    add_parser.add_argument("pages", type=int)
    add_parser.add_argument("deadline")
    add_parser.add_argument("rate", type=int)
    add_parser.add_argument("--urgent", action="store_true")

    subparsers.add_parser("stats", help="Статистика по заказам")

    args = parser.parse_args(argv)

    if args.command == "list":
        return cmd_list(args)
    elif args.command == "add":
        return cmd_add(args)
    elif args.command == "stats":
        return cmd_stats(args)
    return 1
