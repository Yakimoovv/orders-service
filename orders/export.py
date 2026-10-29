from collections.abc import Iterator
from orders.models import Order


def order_rows(orders: list[Order]) -> Iterator[list[str]]:
    yield [
        "№",
        "customer",
        "work_type",
        "pages",
        "deadline",
        "rate",
        "status",
        "urgent",
        "price",
    ]
    for i, order in enumerate(orders, start=1):
        yield [
            str(i),
            order.customer,
            order.work_type,
            str(order.pages),
            order.deadline.isoformat(),
            str(order.rate),
            order.status.value,
            str(order.urgent),
            str(order.price()),
        ]
