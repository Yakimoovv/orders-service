import json

from orders.models import Order, Stats


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

    def to_json(self):
        dict_orders = []
        for order in self.orders:
            dict_orders.append(order.to_dict())
        return json.dumps(dict_orders, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, text, owner):
        dict_orders = json.loads(text)
        book = cls(owner)
        for order in dict_orders:
            order_object = Order.from_dict(order)
            book.add(order_object)
        return book

    def save(self, path):
        with open(path, "w", encoding="UTF-8") as f:
            f.write(self.to_json())
        

    @classmethod
    def load(cls, path, owner):
        with open(path, "r", encoding="UTF-8") as f:
            text = f.read()
        return cls.from_json(text, owner)
        

    def __len__(self):
        return len(self.orders)

