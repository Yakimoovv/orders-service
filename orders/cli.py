import argparse
import sys
from pathlib import Path

from orders.exceptions import StorageError
from orders.storage import OrderBook


def cmd_list(args) -> int:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=Path, default=Path("orders.json"), help="Путь к файлу заказов"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="Список заказов")
    list_parser.add_argument("--status", default=None, help="По статусу")
    list_parser.add_argument("--urgent", action="store_true", help="Только срочные")

    args = parser.parse_args(argv)

    if args.command == "list":
        return cmd_list(args)
    return 1
