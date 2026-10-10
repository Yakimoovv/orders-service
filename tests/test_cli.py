import pytest

from orders.cli import main
from orders.models import Status
from orders.storage import OrderBook


def test_all_orders(tmp_path, book_with_orders, capsys):
    path = tmp_path / "orders.json"
    book_with_orders.save(path)
    result = main(["--file", str(path), "list"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Антон" in captured.out
    assert "Андрей" in captured.out


def test_urgent_orders(tmp_path, book_with_orders, capsys):
    path = tmp_path / "orders.json"
    book_with_orders.save(path)
    result = main(["--file", str(path), "list", "--urgent"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Антон" not in captured.out
    assert "Андрей" in captured.out


def test_file_not_exist(tmp_path, capsys):
    path = tmp_path / "orders.json"

    result = main(["--file", str(path), "list"])
    captured = capsys.readouterr()

    assert result == 1
    assert "не найден" in captured.err
    assert captured.out == ""


def test_not_subcommand(tmp_path):
    path = tmp_path / "orders.json"
    with pytest.raises(SystemExit) as exc_info:
        main(["--file", str(path)])
    assert exc_info.value.code == 2


def test_new_order(tmp_path, book_with_orders):
    path = tmp_path / "orders.json"
    book_with_orders.save(path)
    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "30",
            "2026-10-23",
            "40",
            "--urgent",
        ]
    )
    new_book = OrderBook.load(path, "Глеб")
    new_order = new_book.orders[-1]

    assert result == 0
    assert len(new_book) == len(book_with_orders) + 1
    assert new_order.customer == "Боря"
    assert new_order.work_type == "homework"
    assert new_order.pages == 30
    assert new_order.deadline == "2026-10-23"
    assert new_order.rate == 40
    assert new_order.status == Status.NEW
    assert new_order.urgent is True


def test_file_not_exist_create_new(tmp_path):
    path = tmp_path / "orders.json"
    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "30",
            "2026-10-23",
            "40",
            "--urgent",
        ]
    )
    created_book = OrderBook.load(path, "Глеб")

    assert result == 0
    assert len(created_book) == 1


def test_zero_pages(tmp_path, capsys, book_with_orders):
    path = tmp_path / "orders.json"
    book_with_orders.save(path)
    result = main(
        [
            "--file",
            str(path),
            "add",
            "Боря",
            "homework",
            "0",
            "2026-10-23",
            "40",
            "--urgent",
        ]
    )

    book = OrderBook.load(path, "Глеб")
    captured = capsys.readouterr()

    assert result == 1
    assert "pages" in captured.err
    assert len(book) == 2


def test_corrupted_file(tmp_path, book_with_orders):
    path = tmp_path / "orders.json"
    book_with_orders.save(path)

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
            "2026-10-23",
            "40",
            "--urgent",
        ]
    )

    after = path.read_text(encoding="utf-8")

    assert result == 1
    assert before == after


def test_cmd_stats(tmp_path, book_with_orders, capsys):
    path = tmp_path / "orders.json"
    book_with_orders.save(path)
    result = main(["--file", str(path), "stats"])
    captured = capsys.readouterr()

    assert result == 0
    assert "Всего заказов: 2" in captured.out
    assert "Выручка: 1500" in captured.out
    assert "Срочных: 1" in captured.out
    assert "Типы: {'homework': 2}" in captured.out


def test_cmd_stats_file_not_exist(tmp_path, capsys):
    path = tmp_path / "orders.json"
    result = main(["--file", str(path), "stats"])
    captured = capsys.readouterr()

    assert result == 1
    assert "не найден" in captured.err


def test_wrong_status_in_terminal(tmp_path):
    path = tmp_path / "orders.json"
    with pytest.raises(SystemExit) as exc_info:
        main(["--file", str(path), "list", "--status", "dnoe"])

    assert exc_info.value.code == 2
