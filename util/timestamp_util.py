from datetime import datetime


def datetime_to_string(datetime_object):
    return datetime.isoformat(datetime_object)


def datetime_from_string(text):
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%fZ")


def today():
    return datetime.today()
