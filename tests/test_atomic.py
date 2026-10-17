import pytest

from orders.atomic import AtomicWriter


def test_atomic_writer(tmp_path):
    path = tmp_path / "orders.json"
    text = "текст"
    with AtomicWriter(path) as f:
        f.write(text)
    path_tmp = path.with_name(path.name + ".tmp")
    content = path.read_text(encoding="utf-8")

    assert not path_tmp.exists()
    assert content == text


def test_error_in_atomic_writer(tmp_path):
    path = tmp_path / "orders.json"
    path.write_text("старое", encoding="utf-8")
    with pytest.raises(ValueError):
        with AtomicWriter(path):
            raise ValueError("Сломалось посреди записи")
    text = path.read_text(encoding="utf-8")
    path_tmp = path.with_name(path.name + ".tmp")

    assert text == "старое"
    assert not path_tmp.exists()
