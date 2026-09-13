import math

class Order:
    def __init__(self,  customer, work_type, pages, deadline, rate, status="new", urgent=False):
        self.customer = customer
        self.work_type = work_type
        self.pages = pages
        self.rate = rate
        self.deadline = deadline
        self.status = status
        self.urgent = urgent

    def price(self):
        if self.urgent:
            p = math.ceil(self.pages * self.rate * 1.5)
        else:
            p = self.pages * self.rate
        return p

    def __repr__(self):
        return f"Заказ {self.customer}: объём {self.pages} с. оплата {self.price()} тип {self.work_type}. Выполнить работу к {self.deadline}. Статус: {self.status}"


if __name__ == "__main__":
    first = Order("Глеб", "Конспект", 30, "2026-09-23", 60, "old", False)
    second = Order("Глеб", "Конспект", 30, "2026-09-23", 60, urgent=True)
    third = Order("Глеб", "Конспект", 30, "2026-09-23", 60)
    print(first)
    print(second)
    print(third)

    a = [1,2,3]
    b = [1,2,3]
    print(b is a)
    print(b == a)
    