def join_path(uri, resource_path):
    return '{}{}'.format(uri, resource_path) if resource_path else uri


def filter_dict_by_key(d: dict):
    return {k: v for k, v in d.items() if v}
