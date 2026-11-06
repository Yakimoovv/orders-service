from datetime import date

import pytest

from orders.models import WORK_TYPES, Order, Status
from orders.repository import SqliteOrderRepository
from orders.storage import OrderBook


@pytest.fixture
def order():
    return Order("Антон", WORK_TYPES[1], 20, date.fromisoformat("2099-12-20"), 30)


@pytest.fixture
def urgent_order():
    return Order(
        "Андрей",
        WORK_TYPES[1],
        20,
        date.fromisoformat("2099-12-20"),
        30,
        urgent=True,
        status=Status.DONE,
    )


@pytest.fixture
def book():
    return OrderBook("Андрей")


@pytest.fixture
def book_with_orders(book, order, urgent_order):
    book.add(order)
    book.add(urgent_order)
    return book


@pytest.fixture
def db_with_orders(tmp_path, order, urgent_order):
    path = tmp_path / "orders.db"
    with SqliteOrderRepository(path) as repo:
        repo.add(order)
        repo.add(urgent_order)
    return path
