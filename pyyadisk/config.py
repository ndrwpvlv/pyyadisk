URI = 'https://cloud-api.yandex.net/v1/disk'
RESOURCE_PATH = f'{URI}/resources'
FIELDS_NAME = ['name', 'type', 'path', 'size', 'created', 'modified', 'revision', 'file']
FIELDS = ','.join([f'_embedded.items.{f}' for f in FIELDS_NAME])
FIELDS_FILES = ','.join([f'items.{f}' for f in FIELDS_NAME])
