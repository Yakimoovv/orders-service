from orders.export import order_rows


def test_order_rows(book_with_orders):
    rows = list(order_rows(book_with_orders.orders))
    assert rows == [
        [
            "№",
            "customer",
            "work_type",
            "pages",
            "deadline",
            "rate",
            "status",
            "urgent",
            "price",
        ],
        ["1", "Антон", "homework", "20", "2099-12-20", "30", "new", "False", "600"],
        ["2", "Андрей", "homework", "20", "2099-12-20", "30", "done", "True", "900"],
    ]
