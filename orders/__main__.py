from orders.models import WORK_TYPES, Order
from orders.storage import OrderBook

if __name__ == "__main__":

    a = Order("   Антон    ", WORK_TYPES[1], 30, "2026-03-26", 60, "old")
    b = Order("Антон", WORK_TYPES[1], 10, "2026-03-26", 60)
    c = Order("Андрей", WORK_TYPES[1], 30, "2026-03-26", 60)
    h = Order("Сергей", WORK_TYPES[2], 30, "2026-03-26", 60, urgent=True)

    m = OrderBook("Глеб")
    m.add(a)
    m.add(b)
    m.add(c)
    m.add(h)

    text = m.to_json()
    print(text)

    restored = OrderBook.from_json(text, "Глеб")
    print(len(restored), restored.total_revenue())
    print(restored.orders[0] == m.orders[0])

    m.save("orders.json")

    loaded = OrderBook.load("orders.json", "Глеб")
    print(len(loaded), loaded.total_revenue())
    print(loaded.orders[0] == m.orders[0])


