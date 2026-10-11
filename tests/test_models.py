from datetime import date

import pytest

from orders.models import Order, Status


@pytest.mark.parametrize(
    "pages, rate, urgent, expected",
    [
        (20, 30, False, 600),
        (20, 30, True, 900),
        (19, 59, True, 1682),
        (1, 30, False, 30),
        (1, 29, True, 44),
    ],
)
def test_price(pages, rate, urgent, expected):
    order = Order(
        "Антон", "notes", pages, date.fromisoformat("2026-10-01"), rate, urgent=urgent
    )
    assert order.price() == expected


def test_clean_name():
    order = Order(
        "   Антон   ", "notes", 19, date.fromisoformat("2026-10-01"), 59, urgent=True
    )
    assert order.customer == "Антон"


def test_working_setter():
    order = Order(
        "Антон", "notes", 19, date.fromisoformat("2026-10-01"), 59, urgent=True
    )
    order.pages = 30
    new_price = order.price()
    assert new_price == 2655


def test_converter_dict(urgent_order):
    dict_order = urgent_order.to_dict()
    order_back = Order.from_dict(dict_order)
    assert dict_order == order_back.to_dict()


def test_default_status(order):
    assert order.status is Status.NEW


def test_data_not_obj_data():
    with pytest.raises(TypeError):
        Order("Антон", "notes", 30, "2026-10-01", 60)


@pytest.mark.parametrize(
    "deadline, status, expected",
    [
        (date(2026, 10, 9), Status.NEW, True),
        (date(2026, 10, 10), Status.NEW, False),
        (date(2026, 10, 11), Status.NEW, False),
        (date(2026, 10, 9), Status.IN_PROGRESS, True),
        (date(2026, 10, 9), Status.DONE, False),
        (date(2026, 10, 11), Status.DONE, False),
        (date(2026, 10, 9), Status.CANCELLED, False),
    ],
)
def test_is_overdue(deadline, status, expected):
    today = date(2026, 10, 10)
    order = Order("Антон", "notes", 30, deadline, 60, status=status)
    result = order.is_overdue(today)

    assert result == expected
