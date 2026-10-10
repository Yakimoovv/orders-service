import pytest

from orders.exceptions import StorageCorruptedError, ValidationError
from orders.models import Status
from orders.storage import OrderBook


def test_empty_book(book):
    assert len(book) == 0
    assert book.total_revenue() == 0


def test_different_books_different_orders(order):
    book1 = OrderBook("Антон")
    book2 = OrderBook("Андрей")

    book1.add(order)

    assert len(book2) == 0


def test_outer_list(order):
    list_orders = []
    list_orders.append(order)
    book = OrderBook("Антон", list_orders)
    list_orders.append(order)

    assert len(book) == 1


def test_not_outer_change(order):
    book = OrderBook("Антон")
    book.orders.append(order)

    assert len(book) == 0


def test_can_not_change_orders():
    book = OrderBook("Антон")
    with pytest.raises(AttributeError):
        book.orders = []


def test_not_order_in_list():
    with pytest.raises(TypeError):
        OrderBook("Антон", ["fdgdfg"])


def test_json_converter(book_with_orders):
    str_orders = book_with_orders.to_json()

    book_back = OrderBook.from_json(str_orders, "Антон")
    assert len(book_back) == len(book_with_orders)
    assert book_back.total_revenue() == book_with_orders.total_revenue()


def test_by_status(book_with_orders):
    book_by_status = book_with_orders.by_status(Status.NEW)
    assert len(book_by_status) == 1
    assert book_by_status[0].status == Status.NEW


def test_stats(book_with_orders):
    all_stats = book_with_orders.stats()
    total_orders = all_stats.total_orders
    total_revenue = all_stats.total_revenue
    urgent_count = all_stats.urgent_count
    by_type = all_stats.by_type
    assert total_orders == 2
    assert total_revenue == 1500
    assert urgent_count == 1
    assert by_type == {"homework": 2}


def test_save_and_load(tmp_path, book_with_orders):
    json_file = tmp_path / "orders.json"
    book_with_orders.save(json_file)
    loaded_book = OrderBook.load(json_file, "Глеб")

    assert len(loaded_book) == len(book_with_orders)
    assert loaded_book.to_json() == book_with_orders.to_json()


def test_exist_file(tmp_path, book_with_orders):
    path = tmp_path / "a" / "b" / "orders.json"

    book_with_orders.save(path)
    assert path.exists()


def test_tmp_file_not_exists(tmp_path, book_with_orders):
    path = tmp_path / "a" / "b" / "orders.json"
    book_with_orders.save(path)

    path_tmp = path.with_name(path.name + ".tmp")
    assert not path_tmp.exists()


def test_wrong_status_json(tmp_path):
    path = tmp_path / "orders.json"
    path.write_text(
        '[{"customer": "Антон", "work_type": "homework", "pages": 10, "deadline": "2026-03-26", "rate": 60, "status": "dnoe", "urgent": false}]',
        encoding="utf-8",
    )
    with pytest.raises(StorageCorruptedError) as exc_info:
        OrderBook.load(path, "Антон")
    assert isinstance(exc_info.value.__cause__, ValueError)


def test_wrong_pages_json(tmp_path):
    path = tmp_path / "orders.json"
    path.write_text(
        '[{"customer": "Антон", "work_type": "homework", "pages": 0, "deadline": "2026-03-26", "rate": 60, "status": "done", "urgent": false}]',
        encoding="utf-8",
    )
    with pytest.raises(StorageCorruptedError) as exc_info:
        OrderBook.load(path, "Антон")
    assert isinstance(exc_info.value.__cause__, ValidationError)
