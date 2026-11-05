import sqlite3
from datetime import date
from pathlib import Path

from orders.exceptions import StorageError
from orders.models import Order, Status


class SqliteOrderRepository:
    def __init__(self, path: str | Path) -> None:
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        self._conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer TEXT NOT NULL,
            work_type TEXT NOT NULL,
            pages INTEGER NOT NULL CHECK (pages > 0),
            deadline TEXT NOT NULL,
            rate INTEGER NOT NULL CHECK (rate > 0),
            status TEXT NOT NULL,
            urgent INTEGER NOT NULL
        )""")

    def add(self, order: Order) -> int:
        with self._conn:
            add_order = self._conn.execute(
                "INSERT INTO orders (customer, work_type, pages, deadline, rate, status, urgent) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    order.customer,
                    order.work_type,
                    order.pages,
                    order.deadline.isoformat(),
                    order.rate,
                    order.status.value,
                    int(order.urgent),
                ),
            )
            if add_order.lastrowid is None:
                raise StorageError("Нет ID для нового заказа в SQLite")
        order.id = add_order.lastrowid
        return add_order.lastrowid

    def get(self, order_id: int) -> Order | None:
        row = self._conn.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        if row:
            return self._row_to_order(row)
        else:
            return None

    def _row_to_order(self, row: sqlite3.Row) -> Order:
        return Order(
            customer=row["customer"],
            work_type=row["work_type"],
            pages=row["pages"],
            deadline=date.fromisoformat(row["deadline"]),
            rate=row["rate"],
            status=Status(row["status"]),
            urgent=bool(row["urgent"]),
            id=row["id"],
        )

    def list(self, status: Status | None = None) -> list[Order]:
        list_orders = []
        if status is None:
            rows = self._conn.execute("SELECT * FROM orders ORDER BY id ASC").fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM orders WHERE status = ? ORDER BY id ASC", (status.value,)
            ).fetchall()
        for row in rows:
            list_orders.append(self._row_to_order(row))
        return list_orders

    def close(self) -> None:
        self._conn.close()
