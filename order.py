import math

WORK_TYPES = ('notes', 'homework', 'report')

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
        return f"customer {self.customer}, work_type {self.work_type}, pages {self.pages}, deadline {self.deadline}, rate {self.rate}, status {self.status}, urgent {self.urgent}"

    def __str__(self):
        return f"Заказ {self.customer}: объём {self.pages} с. оплата {self.price()} тип {self.work_type}. Выполнить работу к {self.deadline}. Статус: {self.status}"


if __name__ == "__main__":

    cases = [
        (40, "notes", 40, "2026-09-30", 60),
        ("Антон", "new", 40, "2026-09-30", 60),
        ("Антон", "notes", "40", "2026-09-30", 60),
        ("Антон", "notes", 0, "2026-09-30", 60),
        ("Антон", "notes", 40, "2026-09-30", "балбла"),
        ("  ", "notes", 40, "2026-09-30", 60)
    ]

    for i in cases:
        try:
            a = Order(*i)
        except (ValueError, TypeError) as e:
            print("Не создалось: ", e)
        else:
            print("Ошибка проскочила!!!")


    m = Order("Антон", "notes", 40, "2026-09-30", 60)
    n = Order("Антон", "notes", 40, "2026-09-30", 80, status="оплачен")
    t = Order("Андрей", "notes", 40, "2026-09-30", 80)
    print(m == n)
    print(m == t)

    orders = [m]
    print(n in orders)

    print(m)
    print([m])

    print(m.to_dict())
    print(Order.from_dict(m.to_dict()) == m)