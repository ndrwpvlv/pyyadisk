import json

import requests

from .config import URI, RESOURCE_PATH
from .helpers import filter_dict_by_key


class YandexDisk:
    def __init__(self, token: str = None, proxy: str = None, ssl_verify: bool = True, max_retries: int = 5):
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

        self.params = {'path': None, 'fields': None, 'sort': None, 'limit': None, 'offset': None}

    def path(self, path: str):
        self.params['path'] = path
        return self

    def fields(self, fields: str):
        self.params['fields'] = fields
        return self

    def sort(self, sort):
        self.params['sort'] = sort
        return self

    def add_params(self, key, value):
        self.params[key] = value
        return self

    def get(self, limit: int = None, offset: int = None):
        params = {**self.params, 'limit': limit, 'offset': offset, }
        return self._get(self.resources, filter_dict_by_key(params))

    def create(self, subdir: str = None):
        params = {**self.params, 'path': f'{self.params["path"]}/{subdir}' if subdir else self.params["path"], }
        return self._put(self.resources, filter_dict_by_key(params))

    def delete(self, force_async: bool = None, md5_hash: str = None, permanently: bool = False):
        params = {**self.params, 'force_async': force_async, 'md5': md5_hash, 'permanently': permanently, }
        return self._delete(self.resources, filter_dict_by_key(params))

    def copy(self, destination: str, force_async: bool = None, overwrite: bool = None):
        params = {'from': self.params['path'], 'path': destination, 'fields': self.params['fields'],
                  'force_async': force_async, 'overwrite': overwrite, }
        return self._post(f'{self.resources}/copy', filter_dict_by_key(params))

    def move(self, destination: str, force_async: bool = None, overwrite: bool = None):
        params = {'from': self.params['path'], 'path': destination, 'fields': self.params['fields'],
                  'force_async': force_async, 'overwrite': overwrite, }
        return self._post(f'{self.resources}/move', filter_dict_by_key(params))

    def last_uploaded(self, limit: int = None, media_type: str = None, preview_crop: bool = None,
                      preview_size: str = None):
        params = {'limit': limit, 'media_type': media_type, 'preview_crop': preview_crop,
                  'preview_size': preview_size, }
        return self._get(self.resources, filter_dict_by_key(params))

    def list_files(self, limit: int = None, offset: int = None, media_type: str = None, preview_crop: bool = None,
                   preview_size: str = None):
        params = {'limit': limit, 'offset': offset, 'media_type': media_type, 'preview_crop': preview_crop,
                  'preview_size': preview_size, }
        return self._get(self.resources, filter_dict_by_key(params))

    def link(self):
        try:
            return self._get(f'{self.resources}/download', {'path': self.params.get('path')})[1]['href']
        except Exception as e:
            print(e)
            return None

    def share(self):
        try:
            response = self._put(f'{self.resources}/publish', {'path': self.params.get('path')})
            if response[0] == 200:
                return self.get()[1]["public_url"]
        except Exception as e:
            print(e)
            return None

    def unshare(self):
        try:
            return self._put(f'{self.resources}/unpublish', {'path': self.params.get('path')})[1]['href']
        except Exception as e:
            print(e)
            return None

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
