from datetime import datetime, timedelta


def exp_dict(item):
    out = dict()
    for key, value in item.items():
        if type(value) == dict:
            out[key] = exp_dict(value)
        elif type(value) == int:
            out[key] = int(value)
        else:
            out[key] = str(value)
    return out


def row2dict(row, view_list: list = None):
    d = dict()
    for column in row.__dict__:
        if view_list:
            if column not in view_list:
                continue
        attr = getattr(row, column)
        if type(attr) == list:
            in_list = []
            for item in attr:
                if type(item) == dict:
                    in_record = exp_dict(item)
                    in_list.append(in_record)
                else:
                    in_list.append(str(item))

            d[column] = in_list
        elif type(attr) == dict:
            d[column] = dict()
            d[column] = exp_dict(attr)
        else:
            attr_item = getattr(row, column)
            if type(attr_item) == int:
                d[column] = int(getattr(row, column))
            else:
                d[column] = str(getattr(row, column))
    return d


def dataset2dict(dataset, view_list: list = None):
    result = []
    for row in dataset:
        result.append(row2dict(row, view_list))
    return result


def get_periods():
    now = datetime.now()
    result = list()
    result.append({'name': 'all', 'start': 0, 'end': now})
    result.append({'name': 'day', 'start': now - timedelta(days=1), 'end': now})
    result.append({'name': 'month', 'start': now - timedelta(weeks=4), 'end': now})
    result.append({'name': 'week', 'start': now - timedelta(weeks=1), 'end': now})
    return result
