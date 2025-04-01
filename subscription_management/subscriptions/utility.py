from decimal import Decimal
def serialize_data(data):
    for key, value in data.items():
        if isinstance(value, Decimal):
            data[key] = float(value)
    return data


def get_monthly_cost(subscriptions):
    cost = Decimal(0.0)
    for subs in subscriptions:
        cost = cost + subs.cost
    return cost