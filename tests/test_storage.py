from orders.storage import OrderBook


def test_empty_book(book):
    assert len(book) == 0
    assert book.total_revenue() == 0


def test_different_books_different_orders(order):
    book1 = OrderBook("Антон")
    book2 = OrderBook("Андрей")

    book1.add(order)

    assert len(book2) == 0


def test_json_converter(book_with_orders):
    str_orders = book_with_orders.to_json()

    book_back = OrderBook.from_json(str_orders, "Антон")
    assert len(book_back) == len(book_with_orders)
    assert book_back.total_revenue() == book_with_orders.total_revenue()


def test_by_status(book_with_orders):
    book_by_status = book_with_orders.by_status("new")
    assert len(book_by_status) == 1
    assert book_by_status[0].status == "new"


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
