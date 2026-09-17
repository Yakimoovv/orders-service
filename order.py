import math
from dataclasses import dataclass, field

WORK_TYPES = ('notes', 'homework', 'report')

@dataclass
class Stats:
    total_orders: int
    total_revenue: int
    urgent_count: int
    by_type: dict[str, int] = field(default_factory=dict)

class Order:
    def __init__(self,  customer, work_type, pages, deadline, rate, status="new", urgent=False):
        self.customer = customer
        self.work_type = work_type
        self.pages = pages
        self.rate = rate
        self.deadline = deadline
        self.status = status
        self.urgent = urgent

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя должно быть текстом")
        if value.replace(" ", "") == "":
            raise ValueError("Пустая строка")
        self._customer = value

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        if not isinstance(value, int):
            raise TypeError("Кол-во страниц должно быть целым")
        if value <= 0:
            raise ValueError("Страниц должно быть больше нуля")
        self._pages = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        if not isinstance(value, int):
            raise TypeError("Цена должна быть числом")
        if value <= 0:
            raise ValueError("Цена должна быть больше 0")
        self._rate = value

    @property
    def work_type(self):
        return self._work_type

    @work_type.setter
    def work_type(self, value):
        if value not in WORK_TYPES:
            raise ValueError("Неверный тип работы")
        self._work_type = value

    def price(self): 
        if self.urgent:
            p = math.ceil(self.pages * self.rate * 1.5)
        else:
            p = self.pages * self.rate
        return p

    def to_dict(self):
        return {"customer": self.customer, "work_type": self.work_type, "pages": self.pages, "deadline": self.deadline, "rate": self.rate, "status": self.status, "urgent": self.urgent}

    @classmethod
    def from_dict(cls, data):
        return cls(customer = data['customer'], work_type = data['work_type'], pages = data['pages'], deadline = data['deadline'], rate = data['rate'], status = data['status'], urgent = data['urgent'])


    def __eq__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        return (self.customer, self.work_type, self.pages, self.deadline) == (other.customer, other.work_type, other.pages, other.deadline)

    def __repr__(self):
        return f"Order(customer='{self.customer}', work_type='{self.work_type}', pages={self.pages}, deadline='{self.deadline}', rate={self.rate}, status='{self.status}', urgent={self.urgent})"

    def __str__(self):
        return f"Заказ {self.customer}: объём {self.pages} с. оплата {self.price()} тип {self.work_type}. Выполнить работу к {self.deadline}. Статус: {self.status}"

class OrderBook:

    def __init__(self, owner):
        self.owner = owner
        self.orders = []

    def add(self, order):
        if not isinstance(order, Order):
            raise TypeError('Объект должен быть заказом')
        self.orders.append(order)

    def total_revenue(self):
        full_rate = 0
        for order in self.orders:
            full_rate = order.price() + full_rate
        return full_rate

    def by_status(self, status):
        list_by_status = []
        for order in self.orders:
            if order.status == status:
                list_by_status.append(order)
        return list_by_status

    def stats(self):
        total_orders = len(self.orders)
        total_revenue = 0
        urgent_count = 0
        by_type = {}
        for order in self.orders:
            total_revenue += order.price()
            if order.urgent:
                urgent_count += 1
            by_type[order.work_type] = by_type.get(order.work_type, 0) + 1
        return Stats(total_orders=total_orders, total_revenue=total_revenue, urgent_count=urgent_count, by_type=by_type)


    def __len__(self):
        return len(self.orders)


        



if __name__ == "__main__":

    a = Order("Антон", WORK_TYPES[1], 30, "2026-03-26", 60, "old")
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

    # cases = [
    #     (40, "notes", 40, "2026-09-30", 60),
    #     ("Антон", "new", 40, "2026-09-30", 60),
    #     ("Антон", "notes", "40", "2026-09-30", 60),
    #     ("Антон", "notes", 0, "2026-09-30", 60),
    #     ("Антон", "notes", 40, "2026-09-30", "балбла"),
    #     ("  ", "notes", 40, "2026-09-30", 60)
    # ]

    # for i in cases:
    #     try:
    #         a = Order(*i)
    #     except (ValueError, TypeError) as e:
    #         print("Не создалось: ", e)
    #     else:
    #         print("Ошибка проскочила!!!")


    # m = Order("Антон", "notes", 40, "2026-09-30", 60)
    # n = Order("Антон", "notes", 40, "2026-09-30", 80, status="оплачен")
    # t = Order("Андрей", "notes", 40, "2026-09-30", 80)
    # print(m == n)
    # print(m == t)

    # orders = [m]
    # print(n in orders)

    # print(m)
    # print([m])

    # print(m.to_dict())
    # print(Order.from_dict(m.to_dict()) == m)