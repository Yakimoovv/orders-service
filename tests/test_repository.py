from orders.models import Status
from orders.repository import SqliteOrderRepository


def test_add_order(tmp_path, urgent_order):
    path = tmp_path / "orders.db"
    repo = SqliteOrderRepository(path)
    repo.add(urgent_order)
    order = repo.get(urgent_order.id)

    assert order.to_dict() == urgent_order.to_dict()
    assert order.id == urgent_order.id
    assert repo.get(999) is None


def test_different_status(tmp_path, order, urgent_order):
    path = tmp_path / "orders.db"
    repo = SqliteOrderRepository(path)
    repo.add(urgent_order)
    repo.add(order)

    list_orders = repo.list(Status.DONE)
    assert list_orders[0].customer == "Андрей"
    assert list_orders[0].status == Status.DONE
    assert len(list_orders) == 1
