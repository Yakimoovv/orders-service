from orders.models import WORK_TYPES, Order
from orders.storage import OrderBook


def test_empty_book():
    book = OrderBook("Антон")
    assert len(book) == 0
    assert book.total_revenue() == 0


def test_different_books_different_orders():
    order = Order("Антон", WORK_TYPES[1], 20, "2026-12-30", 30)
    book1 = OrderBook("Антон")
    book2 = OrderBook("Андрей")

    book1.add(order)

    assert len(book2) == 0


def test_json_converter():
    order1 = Order("Антон", WORK_TYPES[1], 20, "2026-12-30", 30)
    order2 = Order("Артем", WORK_TYPES[1], 20, "2026-12-30", 30)
    book = OrderBook("Антон")

    book.add(order1)
    book.add(order2)
    str_orders = book.to_json()

    book_back = OrderBook.from_json(str_orders, "Антон")
    assert len(book_back) == len(book)
    assert book_back.total_revenue() == book.total_revenue()
