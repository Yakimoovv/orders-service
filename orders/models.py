import math
from dataclasses import dataclass, field

from orders.exceptions import ValidationError

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

    @staticmethod
    def normalize_customer(customer):
        return customer.strip()
        
    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя должно быть текстом")
        cleaned_name = self.normalize_customer(value)
        if cleaned_name == "":
            raise ValidationError("customer", "пустая строка")
        self._customer = cleaned_name

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        if not isinstance(value, int):
            raise TypeError("Кол-во страниц должно быть целым")
        if value <= 0:
            raise ValidationError("pages", "должно быть больше нуля")
        self._pages = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        if not isinstance(value, int):
            raise TypeError("Цена должна быть числом")
        if value <= 0:
            raise ValidationError("rate", "должен быть больше 0")
        self._rate = value

    @property
    def work_type(self):
        return self._work_type

    @work_type.setter
    def work_type(self, value):
        if value not in WORK_TYPES:
            raise ValidationError("work_type", f"неверный, допустимы {WORK_TYPES}")
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
