import json

import pytest

from orders.exceptions import (
    StorageCorruptedError,
    StorageNotFoundError,
    ValidationError,
)
from orders.models import WORK_TYPES, Order
from orders.storage import OrderBook


def test_zero_pages():
    with pytest.raises(ValidationError) as exc_info:
        Order("Антон", WORK_TYPES[1], 0, "2026-12-20", 30)
    assert exc_info.value.field == "pages"


def test_one_page():
    order = Order("Антон", WORK_TYPES[1], 1, "2026-12-20", 30)
    assert order.pages == 1


def test_str_page():
    with pytest.raises(TypeError):
        Order("Антон", WORK_TYPES[1], "10", "2026-12-20", 30)


def test_space_name():
    with pytest.raises(ValidationError) as exc_info:
        Order("   ", WORK_TYPES[1], 10, "2026-12-20", 30)
    assert exc_info.value.field == "customer"


def test_wrong_type():
    with pytest.raises(ValidationError):
        Order("Антон", "new", 10, "2026-12-20", 30)


def test_zero_rate():
    with pytest.raises(ValidationError) as exc_info:
        Order("Антон", WORK_TYPES[1], 10, "2026-12-20", 0)
    assert exc_info.value.field == "rate"


def test_wrong_pages():
    order = Order("Антон", WORK_TYPES[1], 10, "2026-12-20", 30)
    with pytest.raises(ValidationError):
        order.pages = -5


def test_not_json():
    with pytest.raises(StorageCorruptedError) as exc_info:
        OrderBook.from_json("это не json", "Глеб")
    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)


def test_file_not_exist():
    with pytest.raises(StorageNotFoundError):
        OrderBook.load("нет_такого_файла.json", "Глеб")


def test_not_real_order():
    book = OrderBook("Глеб")
    with pytest.raises(TypeError):
        book.add("Это не заказ")
