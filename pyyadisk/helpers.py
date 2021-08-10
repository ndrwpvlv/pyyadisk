def join_path(uri, resource_path):
    return '{}{}'.format(uri, resource_path) if resource_path else uri
