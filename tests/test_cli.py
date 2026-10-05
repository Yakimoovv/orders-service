import pytest

from orders.cli import main


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
