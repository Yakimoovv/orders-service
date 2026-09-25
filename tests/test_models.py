from orders.models import Order


def test_price_regular():
    order = Order("Антон", "notes", 10, "2026-10-01", 60)
    assert order.price() == 600


def test_urgent_price():
    order = Order("Антон", "notes", 10, "2026-10-01", 60, urgent=True)
    assert order.price() == 900


def test_float_urgent_price():
    order = Order("Антон", "notes", 19, "2026-10-01", 59, urgent=True)
    assert order.price() == 1682


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
