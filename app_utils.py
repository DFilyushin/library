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


def row2dict(row):
    d = dict()
    for column in row.__dict__:
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


def dataset2dict(dataset):
    result = []
    for row in dataset:
        result.append(row2dict(row))
    return result
