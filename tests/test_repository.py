import sqlite3

import pytest

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


def test_set_status(tmp_path, order):
    path = tmp_path / "orders.db"
    repo = SqliteOrderRepository(path)
    order_id = repo.add(order)

    assert repo.set_status(order_id, Status.DONE) is True
    assert repo.get(order_id).status == Status.DONE
    assert repo.set_status(999, Status.DONE) is False


def test_delete_and_with(tmp_path, order):
    path = tmp_path / "orders.db"
    with SqliteOrderRepository(path) as repo:
        order_id = repo.add(order)
        delete_code = repo.delete(order_id)
        get_unexist_order = repo.get(order_id)
        repeat_delete_code = repo.delete(order_id)

    assert delete_code is True
    assert get_unexist_order is None
    assert repeat_delete_code is False


def test_add_many_rollback(tmp_path, order, urgent_order):
    path = tmp_path / "orders.db"
    urgent_order._pages = 0

    with SqliteOrderRepository(path) as repo:
        with pytest.raises(sqlite3.IntegrityError):
            repo.add_many([order, urgent_order])

        assert repo.list() == []
