import codecs
import csv
from datetime import date

import pytest

from orders.cli import main
from orders.models import WORK_TYPES, Order, Status
from orders.repository import SqliteOrderRepository


def test_all_orders(db_with_orders, capsys):
    path = db_with_orders
    result = main(["--file", str(path), "list"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Антон" in captured.out
    assert "Андрей" in captured.out


def test_urgent_orders(db_with_orders, capsys):
    path = db_with_orders
    result = main(["--file", str(path), "list", "--urgent"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Антон" not in captured.out
    assert "Андрей" in captured.out


def test_file_not_exist(tmp_path, capsys):
    path = tmp_path / "orders.db"

    result = main(["--file", str(path), "list"])
    captured = capsys.readouterr()

    assert result == 1
    assert "не найден" in captured.err
    assert captured.out == ""


def test_not_subcommand(tmp_path):
    path = tmp_path / "orders.db"
    with pytest.raises(SystemExit) as exc_info:
        main(["--file", str(path)])
    assert exc_info.value.code == 2


def test_new_order(db_with_orders):
    path = db_with_orders
    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "30",
            "2099-10-23",
            "40",
            "--urgent",
        ]
    )
    with SqliteOrderRepository(path) as repo:
        orders = repo.list()
    new_order = orders[-1]

    assert result == 0
    assert len(orders) == 3
    assert new_order.customer == "Боря"
    assert new_order.work_type == "homework"
    assert new_order.pages == 30
    assert new_order.deadline == date.fromisoformat("2099-10-23")
    assert new_order.rate == 40
    assert new_order.status == Status.NEW
    assert new_order.urgent is True


def test_file_not_exist_create_new(tmp_path):
    path = tmp_path / "orders.db"
    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "30",
            "2099-10-23",
            "40",
            "--urgent",
        ]
    )
    with SqliteOrderRepository(path) as repo:
        orders = repo.list()

    assert result == 0
    assert len(orders) == 1


def test_zero_pages(db_with_orders, capsys):
    path = db_with_orders
    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "0",
            "2099-10-23",
            "40",
            "--urgent",
        ]
    )

    with SqliteOrderRepository(path) as repo:
        orders = repo.list()
    captured = capsys.readouterr()

    assert result == 1
    assert "pages" in captured.err
    assert len(orders) == 2


def test_corrupted_file(tmp_path):
    path = tmp_path / "orders.db"
    path.write_text("полварпловарп", encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "30",
            "2099-10-23",
            "40",
            "--urgent",
        ]
    )

    after = path.read_text(encoding="utf-8")

    assert result == 1
    assert before == after


def test_cmd_stats(db_with_orders, capsys):
    path = db_with_orders
    result = main(["--file", str(path), "stats"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Всего заказов: 2" in captured.out
    assert "Выручка: 1500" in captured.out
    assert "Срочных: 1" in captured.out
    assert "Типы: {'homework': 2}" in captured.out


def test_cmd_stats_file_not_exist(tmp_path, capsys):
    path = tmp_path / "orders.db"
    result = main(["--file", str(path), "stats"])
    captured = capsys.readouterr()

    assert result == 1
    assert "не найден" in captured.err


def test_wrong_status_in_terminal(tmp_path):
    path = tmp_path / "orders.db"
    with pytest.raises(SystemExit) as exc_info:
        main(["--file", str(path), "list", "--status", "dnoe"])

    assert exc_info.value.code == 2


def test_wrong_add_deadline(tmp_path):
    path = tmp_path / "orders.db"
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--file",
                str(path),
                "add",
                "Боря",
                "homework",
                "30",
                "2026-10-45",
                "40",
                "--urgent",
            ]
        )

    assert exc_info.value.code == 2


def test_past_date(tmp_path):
    path = tmp_path / "orders.db"

    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "30",
            "2000-10-23",
            "40",
            "--urgent",
        ]
    )

    assert result == 1
    assert not path.exists()


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f, delimiter=";"))


def test_export(tmp_path, db_with_orders, capsys):
    path = db_with_orders
    csv_path = tmp_path / "out.csv"

    result = main(["--file", str(path), "export", str(csv_path)])
    captured = capsys.readouterr()

    assert result == 0
    assert "Экспортировано 2 заказов" in captured.out
    assert csv_path.read_bytes().startswith(codecs.BOM_UTF8)
    rows = read_csv(csv_path)
    assert len(rows) == 3
    assert rows[0][0] == "№"
    assert [row[1] for row in rows[1:]] == ["Антон", "Андрей"]


def test_export_by_status(tmp_path, db_with_orders, capsys):
    path = db_with_orders
    csv_path = tmp_path / "out.csv"

    result = main(["--file", str(path), "export", str(csv_path), "--status", "done"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Экспортировано 1 заказов" in captured.out
    rows = read_csv(csv_path)
    assert [row[1] for row in rows[1:]] == ["Андрей"]


def test_export_file_not_exist(tmp_path, capsys):
    path = tmp_path / "orders.db"
    csv_path = tmp_path / "out.csv"

    result = main(["--file", str(path), "export", str(csv_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "не найден" in captured.err
    assert not csv_path.exists()


def test_export_into_orders_file(db_with_orders, capsys):
    path = db_with_orders
    before = path.read_bytes()

    result = main(["--file", str(path), "export", str(path)])
    captured = capsys.readouterr()

    assert result == 1
    assert captured.err != ""
    assert path.read_bytes() == before


def test_different_status(db_with_orders, capsys):
    path = db_with_orders

    result = main(["--file", str(path), "list", "--status", "done"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Андрей" in captured.out
    assert "Антон" not in captured.out


def test_overdue_orders(tmp_path, capsys):
    path = tmp_path / "orders.db"
    order1 = Order("Антон", WORK_TYPES[1], 30, date(2000, 1, 1), 20, status=Status.NEW)
    order2 = Order(
        "Андрей", WORK_TYPES[1], 30, date(2000, 1, 1), 20, status=Status.DONE
    )
    order3 = Order("Сергей", WORK_TYPES[1], 30, date(2099, 12, 20), 20)
    with SqliteOrderRepository(path) as repo:
        for order in [order1, order2, order3]:
            repo.add(order)

    result = main(["--file", str(path), "list", "--overdue"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Антон" in captured.out
    assert ("Андрей" not in captured.out) and ("Сергей" not in captured.out)


def test_status(db_with_orders, capsys):
    path = db_with_orders
    result = main(["--file", str(path), "status", "1", "done"])
    captured = capsys.readouterr()

    with SqliteOrderRepository(path) as repo:
        order = repo.get(1)

    assert result == 0
    assert "статус done" in captured.out
    assert order.status == Status.DONE


def test_status_not_found(db_with_orders, capsys):
    path = db_with_orders
    result = main(["--file", str(path), "status", "999", "done"])
    captured = capsys.readouterr()

    assert result == 1
    assert "не найден" in captured.err


def test_delete(db_with_orders, capsys):
    path = db_with_orders
    first = main(["--file", str(path), "delete", "1"])
    second = main(["--file", str(path), "delete", "1"])
    captured = capsys.readouterr()

    with SqliteOrderRepository(path) as repo:
        orders = repo.list()

    assert first == 0
    assert second == 1
    assert "не найден" in captured.err
    assert len(orders) == 1


def test_migrate_twice(tmp_path, book_with_orders, capsys):
    json_path = tmp_path / "orders.json"
    db_path = tmp_path / "orders.db"
    book_with_orders.save(json_path)

    first = main(["--file", str(db_path), "migrate", str(json_path)])
    second = main(["--file", str(db_path), "migrate", str(json_path)])
    captured = capsys.readouterr()

    with SqliteOrderRepository(db_path) as repo:
        orders = repo.list()

    assert first == 0
    assert second == 1
    assert "не пуста" in captured.err
    assert len(orders) == 2
