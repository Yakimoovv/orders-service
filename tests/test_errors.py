import json

import pytest

from orders.exceptions import (
    StorageCorruptedError,
    StorageNotFoundError,
    ValidationError,
)
from orders.models import WORK_TYPES, Order
from orders.storage import OrderBook


@pytest.mark.parametrize("pages", [0, -1, -100])
def test_wrong_amount_pages(pages):
    with pytest.raises(ValidationError) as exc_info:
        Order("Антон", WORK_TYPES[1], pages, "2026-12-20", 30)
    assert exc_info.value.field == "pages"


def test_one_page():
    order = Order("Антон", WORK_TYPES[1], 1, "2026-12-20", 30)
    assert order.pages == 1


@pytest.mark.parametrize("pages", ["10", 1.5, None, True])
def test_wrong_type_page(pages):
    with pytest.raises(TypeError):
        Order("Антон", WORK_TYPES[1], pages, "2026-12-20", 30)


def test_space_name():
    with pytest.raises(ValidationError) as exc_info:
        Order("   ", WORK_TYPES[1], 10, "2026-12-20", 30)
    assert exc_info.value.field == "customer"


@pytest.mark.parametrize("work_type", ["NOTES", "essay", ""])
def test_wrong_type(work_type):
    with pytest.raises(ValidationError):
        Order("Антон", work_type, 10, "2026-12-20", 30)


@pytest.mark.parametrize("rate", ["60", 1.5, None, True])
def test_wrong_rate(rate):
    with pytest.raises(TypeError):
        Order("Антон", WORK_TYPES[1], 10, "2026-12-20", rate)


def test_zero_rate():
    with pytest.raises(ValidationError) as exc_info:
        Order("Антон", WORK_TYPES[1], 10, "2026-12-20", 0)
    assert exc_info.value.field == "rate"


def test_wrong_pages(order):
    with pytest.raises(ValidationError):
        order.pages = -5


def test_not_json():
    with pytest.raises(StorageCorruptedError) as exc_info:
        OrderBook.from_json("это не json", "Глеб")
    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)


def test_corrupted_json(tmp_path):
    path = tmp_path / "orders.json"
    path.write_text("это не json", encoding="utf-8")
    with pytest.raises(StorageCorruptedError) as exc_info:
        OrderBook.load(path, "Глеб")
    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)


def test_file_not_exist(tmp_path):
    with pytest.raises(StorageNotFoundError):
        OrderBook.load(tmp_path / "missing.json", "Глеб")


def test_not_real_order(book):
    with pytest.raises(TypeError):
        book.add("Это не заказ")


def test_wrong_encoding(tmp_path):
    path = tmp_path / "orders.json"
    path.write_text('[{"customer": "Антон"}]', encoding="cp1251")
    with pytest.raises(StorageCorruptedError) as exc_info:
        OrderBook.load(path, "Глеб")
    assert isinstance(exc_info.value.__cause__, UnicodeDecodeError)


def test_no_field_in_order(tmp_path):
    path = tmp_path / "orders.json"
    path.write_text(
        '[{"customer": "Антон","work_type": "homework","deadline": "2026-03-26","rate": 60,"status": "old","urgent": false}]',
        encoding="utf-8",
    )

    with pytest.raises(StorageCorruptedError) as exc_info:
        OrderBook.load(path, "Глеб")
    assert isinstance(exc_info.value.__cause__, KeyError)
