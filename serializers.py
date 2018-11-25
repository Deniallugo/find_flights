from datetime import datetime


def isnamedtuple(value):
    return isinstance(value, tuple) and hasattr(value, '_asdict')


def serialize_dict(data: dict):
    for key, value in data.items():
        data[key] = serialize(value)
    return data


def serialize(value):
    """
    Very simple implementation of serializer
    :param value:
    :return:
    """
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, list):
        return [serialize(item) for item in value]
    elif isnamedtuple(value):
        return serialize_dict(value._asdict())
    elif isinstance(value, dict):
        return serialize_dict(value)
    else:
        return value
