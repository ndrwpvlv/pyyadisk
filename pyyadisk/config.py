URI = 'https://cloud-api.yandex.net/v1/disk'
RESOURCE_PATH = f'{URI}/resources'
JSON_ROOT = '_embedded.items'
FIELDS_NAME = ['name', 'type', 'size', 'created', 'modified', 'revision']
FIELDS = ','.join([f'{JSON_ROOT}.{f}' for f in FIELDS_NAME])
METHODS = {
    'get': {'code': 200, },
    'put': {'code': 201, },
    'post': {'code': 200, },
    'delete': {'code': 204, },
}
