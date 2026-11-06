from orders.export import order_rows


def test_order_rows(book_with_orders):
    orders = book_with_orders.orders
    orders[0].id = 5
    rows = list(order_rows(orders))
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
        ["5", "Антон", "homework", "20", "2099-12-20", "30", "new", "False", "600"],
        ["", "Андрей", "homework", "20", "2099-12-20", "30", "done", "True", "900"],
    ]
