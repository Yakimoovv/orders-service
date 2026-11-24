from pathlib import Path

from fastapi import FastAPI

from orders.repository import SqliteOrderRepository

DB_PATH = Path("orders.db")

app = FastAPI(title="orders-service")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/orders")
def list_orders() -> list[dict]:
    with SqliteOrderRepository(DB_PATH) as repo:
        orders = repo.list()
    return [{"id": order.id, **order.to_dict()} for order in orders]
