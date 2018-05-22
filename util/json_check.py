import re

splitter = re.compile('[, ]+')


class FieldNotFoundError(Exception):
    pass


def check_fields(json, fields: str):
    """
    Check if every fields are in json, and return them with the order in fields
    :param json: dict to be checked
    :param fields: field names separated by ', '
    :return: list of values in order
    """
    fields = splitter.split(fields.strip(', '))
    if any([key not in json for key in fields]):
        raise FieldNotFoundError('required parameters not complete\nNeed: {}\nGot : {}'.format(
            ', '.join(fields), ', '.join(list(json.keys()))))
    return [json[key] for key in fields]