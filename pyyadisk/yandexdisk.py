import json
import requests
from .config import URI, RESOURCE_PATH, FIELDS


class YandexDisk:
    def __init__(self, token: str = None, proxy: str = None, ssl_verify=True, max_retries: int = 5):
        self.token = token
        self.headers = {'Authorization': 'OAuth {}'.format(self.token), 'Accept': 'application/json'}

        if proxy:
            self.proxies = {'http': proxy, 'https': proxy, }
        else:
            self.proxies = None
        self.session = requests.Session()
        self.session_adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount('http://', self.session_adapter)
        self.session.mount('https://', self.session_adapter)
        self.ssl_verify = ssl_verify

        self.uri = URI
        self.resources = RESOURCE_PATH
        self.json_fields = FIELDS

    def get_info(self, path_: str = None, fields: str = None, limit: int = None, offset: int = None,
                 preview_crop: bool = None, preview_size: str = None, sort: str = 'name'):
        if not path_:
            return self._get(self.uri)
        params = {'path': path_, 'fields': fields or self.json_fields, 'limit': limit, 'offset': offset,
                  'preview_crop': preview_crop, 'preview_size': preview_size, 'sort': sort}
        return self._get(self.resources, params)

    def listdir(self, path_: str = '/', fields: str = None, limit: int = None, offset: int = None, sort='name'):
        params = {'path': path_, 'fields': fields or self.json_fields, 'limit': limit, 'offset': offset, 'sort': sort}
        return self._get(self.resources, params)

    def mkdir(self, path_: str, fields: str = 'href'):
        params = {'path': path_, 'fields': fields}
        return self._put(self.resources, params)

    def copy(self, source: str, destination: str, fields: str = None, force_async: bool = None, overwrite: bool = None):
        params = {'from': source, 'path': destination, 'fields': fields, 'force_async': force_async, 'overwrite': overwrite, }
        return self._post(f'{self.resources}/copy', params)

    def move(self, source: str, destination: str, fields: str = None, force_async: bool = None, overwrite: bool = None):
        params = {'from': source, 'path': destination, 'fields': fields, 'force_async': force_async, 'overwrite': overwrite, }
        return self._post(f'{self.resources}/move', params)

    def remove(self, path_: str, fields: str = None, force_async: bool = None, md5_hash: str = None, permanently: bool = False):
        params = {'path': path_, 'fields': fields, 'force_async': force_async, 'md5': md5_hash, 'permanently': permanently, }
        return self._delete(self.resources, params)

    def get_download_link(self, path_: str, fields: str = None):
        params = {'path': path_, 'fields': fields, }
        return self._get(f'{self.resources}/download', params)

    def _get(self, uri: str, params: dict = None):
        return self._request('get', uri=uri, params=params)

    def _post(self, uri: str, params: dict = None):
        return self._request('post', uri=uri, params=params)

    def _put(self, uri: str, params: dict = None):
        return self._request('put', uri=uri, params=params)

    def _delete(self, uri: str, params: dict = None):
        return self._request('delete', uri=uri, params=params)

    def _request(self, method: str, uri: str, params: dict = None):
        data = None
        try:
            response = getattr(self.session, method)(uri, headers=self.headers, verify=self.ssl_verify,
                                                     proxies=self.proxies, params=params)
            if 200 <= response.status_code <= 299:
                try:
                    data = response.json()
                except json.decoder.JSONDecodeError:
                    pass
                return response.status_code, data
            else:
                print('Code {}'.format(response.status_code))
            return response.status_code, data
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
