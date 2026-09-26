import pytest

from orders.models import Order


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
    order = Order("Антон", "notes", pages, "2026-10-01", rate, urgent=urgent)
    assert order.price() == expected


def test_clean_name():
    order = Order("   Антон   ", "notes", 19, "2026-10-01", 59, urgent=True)
    assert order.customer == "Антон"


def test_working_setter():
    order = Order("Антон", "notes", 19, "2026-10-01", 59, urgent=True)
    order.pages = 30
    new_price = order.price()
    assert new_price == 2655


def test_converter_dict():
    order = Order("Антон", "notes", 19, "2026-10-01", 59, urgent=True)
    dict_order = order.to_dict()
    order_back = Order.from_dict(dict_order)
    assert order == order_back
