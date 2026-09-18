from orders.exceptions import OrderError, ValidationError
from orders.models import WORK_TYPES, Order, Stats
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
    print(m.total_revenue())
    print(len(m))
    print(m.by_status("new"))

    try:
        m.add('не заказ')
    except TypeError as e:
        print('Поймано:', e)

    empty = OrderBook("Глеб")
    print(len(empty))
    print(empty.total_revenue())
    print(empty.by_status("new"))
    print(m.stats())
    print(empty.stats())
    print(m.stats() == m.stats())
    print(Stats(0, 0, 0))

    print(Order.normalize_customer("  Антон  "))
    print(repr(a.customer))
    try:
        Order("   ", WORK_TYPES[2], 30, "2029-10-20", 60)
    except ValidationError as e:
        print("Ошибка", e)

    try:
        Order("   ", WORK_TYPES[2], 30, "2029-10-20", 60)
    except OrderError as e:
        print("Ошибка", e)

    try:
        Order(123, WORK_TYPES[2], 30, "2029-10-20", 60)
    except TypeError as e:
        print("Ошибка", e)

print(issubclass(ValidationError, OrderError))
print(issubclass(ValidationError, Exception))
print(issubclass(OrderError, ValidationError))
