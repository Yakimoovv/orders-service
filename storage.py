from models import Order, Stats

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

