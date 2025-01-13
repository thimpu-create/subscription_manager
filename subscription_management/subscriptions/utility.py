from decimal import Decimal
def serialize_data(data):
    for key, value in data.items():
        if isinstance(value, Decimal):
            data[key] = float(value)
    return data