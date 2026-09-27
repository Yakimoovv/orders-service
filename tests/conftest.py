import pytest

from orders.models import WORK_TYPES, Order
from orders.storage import OrderBook


@pytest.fixture
def order():
    return Order("Антон", WORK_TYPES[1], 20, "2026-12-20", 30)


@pytest.fixture
def urgent_order():
    return Order(
        "Андрей", WORK_TYPES[1], 20, "2026-12-20", 30, urgent=True, status="old"
    )


@pytest.fixture
def book():
    return OrderBook("Андрей")


@pytest.fixture
def book_with_orders(book, order, urgent_order):
    book.add(order)
    book.add(urgent_order)
    return book
