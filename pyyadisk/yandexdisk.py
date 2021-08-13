import json
from pathlib import Path

import requests

from .config import URI, RESOURCES_PATH, TRASH_PATH, OPERATIONS_PATH
from .helpers import filter_dict_by_key


class YandexDisk:
    """Yandex Disk Rest API V1 wrapper

    Python realisation of Yandex Disk Rest API V1 wrapper:
    - OAuth authorization by token
    Resources:
    - Get metadata of file or directory
    - Create directory
    - Delete file or directory
    - Move file or directory
    - Copy file or directory
    - Get download link (private)
    - Share directory or file and get public link
    - Get download link (public)
    - Get list of files
    - Get last uploaded files
    - Upload file
    - Upload file by url
    Trash:
    - Empty
    - Delete files
    - Restore files
    Async operations status

    Attributes:
        token: Oauth token (get it at https://yandex.ru/dev/disk/poligon/)
        headers: Dictionary with headers ('Authorization', 'Accept')
        proxies: (optional) Dictionary with proxy addresses for http and https
        session: Object of requests.Session()
        ssl_verify: (optional) Flag of connection ssl verification check
        uri: Yandex Disk Rest API endpoint uri
        resources: Yandex Disk Rest API resources uri
        params: Dictionary to send in the query string for the Request
    """

    def __init__(self, token: str = None, proxy: str = None, ssl_verify: bool = True, max_retries: int = 5):
        """
        Initialization of YandexDisk REST API V1 wrapper class

        Args:
            token: Oauth token (get it at https://yandex.ru/dev/disk/poligon/)
            proxy: (optional) Proxy address for http and https
            ssl_verify: (optional) Flag of connection ssl verification check
            max_retries: (optional) Number of maximum connection retries
        """
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
        self.resources = RESOURCES_PATH

        self.params = {'path': None, 'fields': None, 'sort': None, 'limit': None, 'offset': None}

    def trash(self, path: str = None):
        """
        Enter to the Trash mode.

        Typical usage example:
            disk = YandexDisk()
            trash_ = disk.trash('path/to/the/file')

        Args:
            path: The full path to the resource in the Trash (file or directory). Get the root with path = '/' or None

        Returns:
            Self YandexDisk object
        """
        self.resources = TRASH_PATH
        self.params['path'] = path
        return self

    def restore(self, name: str = None, force_async: bool = None, overwrite: bool = False):
        """
        Restore trash items

        Typical usage example:
            disk = YandexDisk()
            trash_ = disk.trash('path/to/the/file.pdf')
            response = trash_.restore()

        Args:
            name: The name under which the resource will be restored.
            force_async: Execute asynchronously (True or False).
            overwrite: Overwrite the existing resource with the restored one  (True or False).

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)

            JSON Response dict:
                {
                  "href": "string",
                  "method": "string",
                  "templated": true
                }
        """
        params = {**self.params, 'name': name, 'force_async': force_async, 'overwrite': overwrite, }
        return self._put(f'{self.resources}/restore', params=filter_dict_by_key(params))

    def operations(self, operation_id: str):
        """
        Get the status of an asynchronous operation

        Typical usage example:
            disk = YandexDisk()
            response = disk.operations('aabbccdd')

        Args:
            operation_id: Operation Id

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)

            JSON Response dict:
                {
                  "status": "string"
                }
        """
        params = {'operation_id': operation_id}
        return self._get(f'{OPERATIONS_PATH}/{operation_id}', params=params)

    def path(self, path: str = None):
        """
        Enter to the Disk mode

        Typical usage example:
            disk = YandexDisk()
            path_ = disk.path('path/to/the/file.pdf')

        Args:
            path: The full path of the Disk resource (file or directory)

        Returns:
            Self YandexDisk object
        """
        self.resources = RESOURCES_PATH
        self.params['path'] = path
        return self

    def fields(self, fields: str = None):
        """
        Add filter fields of JSON elements.

        Typical usage example:
            disk = YandexDisk()
            path_ = disk.path('path/to/the/file.pdf')
            path_.fields(fields='_embedded.items.name,_embedded.items.size')

        Args:
            fields: string with fields names. For example fields = '_embedded.items.name,_embedded.items.size'

        Returns:
            Self YandexDisk object
        """
        self.params['fields'] = fields
        return self

    def sort(self, sort: str = None):
        """
        Set an attribute by which to sort the list of resources:
        - name
        - path
        - created
        - modified
        - size

        Typical usage example:
            disk = YandexDisk()
            path_ = disk.path('path/to/the/file.pdf')
            path_.sort(sort='name')

        Args:
            sort: The attribute by which to sort the list of resources

        Returns:
            Self YandexDisk object
        """
        self.params['sort'] = sort
        return self

    def add_param(self, key, value):
        """
        Add any parameter to request params dictionary

        Typical usage example:
            disk = YandexDisk()
            disk.add_param('sort': 'name')

        Args:
            key: The key of parameter
            value: The value of parameter

        Returns:
            Self YandexDisk object
        """
        self.params[key] = value
        return self

    def add_params(self, params: dict):
        """
        Add dictionary with parameters to request params dictionary

        Typical usage example:
            disk = YandexDisk()
            disk.add_params({'sort': 'name', })

        Args:
            params: Dictionary with parameters

        Returns:
            Self YandexDisk object
        """
        self.params.update(params)
        return self

    def get(self, limit: int = None, offset: int = None):
        """
        Make get metadata of file or directory from Disk or Trash mode. For objects sorting use YandexDisk.sort() method

        Typical usage example:
            disk = YandexDisk()
            info = disk.path('path/to/the/file').get()

        Args:
            limit: The number of items to return
            offset: Offset from the beginning

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {**self.params, 'limit': limit, 'offset': offset, }
        return self._get(self.resources, params=filter_dict_by_key(params))

    def create(self, subdir: str = None):
        """
        Make directory or subdirectory by the path

        Typical usage example:
            disk = YandexDisk()
            dir_ = disk.path('path/to/the/directory').create()  # create the directory by the path
            dir_ = disk.path('path/to/the/directory').create('subdirectory')  # create the subdirectory in the directory

        or

            disk = YandexDisk()
            directory = disk.path('path/to/the/directory')
            subdir_list = ['sub_1', 'sub_2', 'sub_3', 'sub_4', ]
            for s in subdir_list:
                directory.create(s)

        Args:
            subdir: Name of subdirectory. If 'subdir = None' the directory will be created by path-data

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {**self.params, 'path': f'{self.params["path"]}/{subdir}' if subdir else self.params["path"], }
        return self._put(self.resources, params=filter_dict_by_key(params))

    def delete(self, force_async: bool = None, md5_hash: str = None, permanently: bool = False):
        """
        Delete file or directory by path from Disk or Trash mode

        Typical usage example:
            disk = YandexDisk()
            directory = disk.path('path/to/the/directory').delete()

        Args:
            force_async: Execute asynchronously (True or False).
            md5_hash: md5 hash of file
            permanently: Flag of permanently delete

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {**self.params, 'force_async': force_async, 'md5': md5_hash, 'permanently': permanently, }
        return self._delete(self.resources, params=filter_dict_by_key(params))

    def copy(self, destination: str, force_async: bool = None, overwrite: bool = None):
        """
        Copy file or directory to new destination

        Typical usage example:
            disk = YandexDisk()
            directory = disk.path('path/to/the/old_directory')
            directory.copy('path/to/the/new_directory_1')
            directory.copy('path/to/the/new_directory_2')  # Nice way to make multiple copies

        Args:
            destination: Destination path
            force_async: Execute asynchronously (True or False).
            overwrite: Flag of overwrite enable

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {'from': self.params['path'], 'path': destination, 'fields': self.params['fields'],
                  'force_async': force_async, 'overwrite': overwrite, }
        return self._post(f'{self.resources}/copy', params=filter_dict_by_key(params))

    def move(self, destination: str, force_async: bool = None, overwrite: bool = None):
        """
        Move file or directory to new destination

        Typical usage example:
            disk = YandexDisk()
            directory = disk.path('path/to/the/old_directory')
            directory.move('path/to/the/new_directory_1')

        Args:
            destination: Destination path
            force_async: Execute asynchronously (True or False).
            overwrite: Flag of overwrite enable

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {'from': self.params['path'], 'path': destination, 'fields': self.params['fields'],
                  'force_async': force_async, 'overwrite': overwrite, }
        return self._post(f'{self.resources}/move', params=filter_dict_by_key(params))

    def last_uploaded(self, limit: int = None, media_type: str = None, preview_crop: bool = None,
                      preview_size: str = None):
        """
        Get list of last uploaded files

        Args:
            limit: The number of items to return
            media_type: Filter by media type
            preview_crop: Enable crop preview
            preview_size: Size of preview

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {'limit': limit, 'media_type': media_type, 'preview_crop': preview_crop,
                  'preview_size': preview_size, }
        return self._get(self.resources, params=filter_dict_by_key(params))

    def list_files(self, limit: int = None, offset: int = None, media_type: str = None, preview_crop: bool = None,
                   preview_size: str = None):
        """
        Get list of files. For objects sorting use YandexDisk.sort() method

        Args:
            limit: The number of items to return
            offset: Offset from the beginning
            media_type: Filter by media type
            preview_crop: Enable crop preview
            preview_size: Size of preview

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {'limit': limit, 'offset': offset, 'media_type': media_type, 'preview_crop': preview_crop,
                  'preview_size': preview_size, }
        return self._get(self.resources, params=filter_dict_by_key(params))

    def link(self):
        """
        Get private link of file or directory which set by YandexDisk.path('path/to/the/file')

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        try:
            return 200, self._get(f'{self.resources}/download', {'path': self.params.get('path')})[1]['href']
        except TypeError:
            return 404, None

    def share(self):
        """
        Share file or directory which set by YandexDisk.path('path/to/the/file')

        Returns:
            tuple(response code, public url) or tuple(404, None) for any errors cases
        """
        response = self._put(f'{self.resources}/publish', {'path': self.params.get('path')})
        if response[0] == 200:
            return response[0], self.get()[1]["public_url"]
        return 404, None

    def unshare(self):
        """
        Unshare public file of directory which set by YandexDisk.path('path/to/the/file')

        Returns:
            tuple(404, None) for any errors cases
        """
        try:
            return self._put(f'{self.resources}/unpublish', {'path': self.params.get('path')})[1]['href']
        except TypeError:
            return 404, None

    def public_url(self):
        """
        Get public url of public file of directory which set by YandexDisk.path('path/to/the/file')

        Returns:
            tuple(response code, public url)  or tuple(404, None) for any errors cases
        """
        try:
            return self._get(self.resources, filter_dict_by_key(self.params))[1]['public_url']
        except KeyError:
            return 404, None

    def public_key(self):
        """
        Get public key of public file of directory which set by YandexDisk.path('path/to/the/file')

        Returns:
            tuple(response code, public key) or tuple(404, None) for any errors cases
        """
        try:
            return self._get(self.resources, filter_dict_by_key(self.params))[1]['public_key']
        except KeyError:
            return 404, None

    def upload(self, filepath: str, overwrite: bool = False):
        """
        File upload method

        Args:
            filepath: Path to the file
            overwrite: Enable overwriting for uploaded item

        Returns:
            tuple(response code, response) or tuple(404, None) for any errors cases
        """
        filename = Path(filepath).name
        path = f'{self.params["path"]}/{filename}'
        try:
            link = self._get_upload_link(path=path, overwrite=overwrite)
            if link:
                files = {'file': open(filepath, 'rb')}
                params = {**self.params, 'path': path}
                return self._put(link, files=files, params=params)
            else:
                return 404, None
        except FileNotFoundError as e:
            return 404, str(e)

    def upload_by_url(self, filename: str, url: str, disable_redirects: bool = False):
        """
        Upload file from the web by url to the path which set by YandexDisk.path('path/to/the/file')

        Args:
            filename: name of the file
            url: url of the file
            disable_redirects: Disable redirects

        Returns:
            Tuple with Response code and dictionary from JSON:
            (Response code, JSON Response dict or None for error)
        """
        params = {**self.params, 'path': f'{self.params["path"]}/{filename}', 'url': url,
                  'disable_redirects': disable_redirects}
        return self._post(f'{self.resources}/upload', params=filter_dict_by_key(params))

    def _get_upload_link(self, path: str, overwrite: bool = False):
        """
        Get upload link for YandexDisk.upload() method

        Args:
            path: Full path to the file or directory on Yandex Disk
            overwrite: Enable overwriting for uploaded item

        Returns:

        """
        params = {**self.params, 'path': path, 'overwrite': overwrite, }
        try:
            return self._get(f'{self.resources}/upload', params=filter_dict_by_key(params))[1]['href']
        except (KeyError, TypeError):
            return None

    def _get(self, uri: str, params: dict = None):
        return self._request('get', uri=uri, params=params)

    def _post(self, uri: str, params: dict = None, data: dict = None):
        return self._request('post', uri=uri, params=params, data=data)

    def _put(self, uri: str, params: dict = None, files: dict = None):
        return self._request('put', uri=uri, params=params, files=files)

    def _delete(self, uri: str, params: dict = None):
        return self._request('delete', uri=uri, params=params)

    def _request(self, method: str, uri: str, params: dict = None, files: dict = None, data: dict = None):
        json_data = None
        try:
            response = getattr(self.session, method)(uri, headers=self.headers, verify=self.ssl_verify,
                                                     proxies=self.proxies, params=params, files=files, data=data)
            if 200 <= response.status_code <= 299:
                try:
                    json_data = response.json()
                except json.decoder.JSONDecodeError:
                    pass
                return response.status_code, json_data
            else:
                pass
            return response.status_code, json_data
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
