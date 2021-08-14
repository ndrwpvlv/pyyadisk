# PyYaDisk
**PyYaDisk** is a wrapper over Yandex Disk Rest API V1. 
The library is in creation process. You can check realized features with our roadmap below. 

## Installation
Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):
```
pip install -U pyyadisk
```
For direct installation from Github
```
pip install git+https://github.com/ndrwpvlv/pyyadisk.git
```

## Usage

### 0. Get Oauth-token
Before you start using YandexDisk API, you need to get a token for Oauth authorization.
You can get it from [Yandex Poligon](https://yandex.ru/dev/disk/poligon/).

### 1. Yandex Disk instance
Let's start. At first we need to make an YandexDisk instance:
```python
from pyyadisk import YandexDisk

token = 'ya_oauth_token'
disk = YandexDisk(token=token, proxy=proxy, ssl_verify=True, max_retries=5)
```
`token`: Oauth token (get it at [https://yandex.ru/dev/disk/poligon/](https://yandex.ru/dev/disk/poligon/))

`proxy`: (optional) Proxy address for http and https

`ssl_verify`: (optional) Flag of connection ssl verification check

`max_retries`: (optional) Number of maximum connection retries


### 2. Set Path
Now we ready to make some operations. Let's set the path for operations:

```python
disk.path(path='path/to/directory')
```
`path`: full path to directory or file

### 3. Upload a file

#### 3.1. Upload local file
Ok. We ready to upload a file from computer. 
If file exists it will be overwritten with flag `overwrite=True`

```python
disk = YandexDisk(token=token)
disk.path(path='path/to/directory')
response = disk.upload(filepath='home/computer/path/to/the/file.pdf', overwrite=True)
```
`filepath`: Path to the file

`overwrite`: (optional) Enable overwriting for uploaded item

Or in one line
```python
disk.path('path/to/directory').upload('home/computer/path/to/the/file.pdf', overwrite=True)
```

#### 3.2. Upload file by URL
```python
disk = YandexDisk(token=token)
disk.path(path='path/to/directory')
operation_id = disk.upload_by_url(filename='file.pdf', url='https://example.com/file_1.pdf', disable_redirects=False)
```
Uploading file by url working at serverside in async mode. ```upload_by_url()``` returns `operation_id`.

`filename`: name of the file

`url`: url of the file

`disable_redirects`: Disable redirects

### 4. Uploading status
By `operation_id` we can get status of uploading:
```python
status = disk.operations(self, operation_id: str)
```

### 5. File or Directory operations
Now when file or directory was uploaded we can make some operations with it.

* `get(limit: int = None, offset: int = None)`: Get stats of file or directory

    `limit`: The number of items to return
    
    `offset`: Offset from the beginning


* `create(self, subdir: str = None)`: Create directory

    `subdir`: Name of subdirectory. If 'subdir = None' the directory will be created by path-data


* `delete(self, force_async: bool = None, md5_hash: str = None, permanently: bool = False)`: Delete file or directory
  
    `force_async`: Execute asynchronously (True or False).

    `md5_hash`: md5 hash of file

    `permanently`: Flag of permanently delete


* `copy_to(self, destination: str, force_async: bool = None, overwrite: bool = None)`: Copy file or directory
* `move_to(self, destination: str, force_async: bool = None, overwrite: bool = None)`: Move file or directory

    `destination`: Destination path

    `force_async`: Execute asynchronously (True or False).

    `overwrite`: Flag of overwrite enable


```python
disk = YandexDisk(token=token)

create_ = disk.path('path/to/directory').create()  # Create directory

info = disk.path('path/to/directory').get()  # Directory stats

copy_ = disk.path('path/to/directory').copy_to('path/to/new/directory')  # Copy from path='path/to/directory'

move_ = disk.path('path/to/directory').move_to('path/to/new/directory')  # Move from path='path/to/directory'

disk.path('path/to/directory').delete()  # Delete directory or file
```

### 6. Share

`share()`: Share file or directory which set by YandexDisk.path('path/to/the/file'). Returns `tuple(response_code, public_url)`

`unshare()`: Unshare file or directory

`public_url()`: Get public url of file or directory

`public_key()`: Get public key of file or directory

Example:

```python
disk = YandexDisk(token=token)

link = disk.path('path/to/directory').share()
link = disk.path('path/to/directory').public_url()
public_key = disk.path('path/to/directory').public_key()
disk.path('path/to/directory').unshare()
```

## Roadmap
* OAuth authorization by token

`/v1/disk`
* Get disk metadata

`/v1/disk/resources`
* Get metadata of file or directory
* Create directory
* Delete file or directory
* Move file or directory
* Copy file or directory
* Get download link (private)
* Share directory or file and get public link
* Get download link (public)
* Get list of files
* Get last uploaded files
* Upload file
* Upload file by url

`/v1/disk/resources/save-to-disk`
- (In process) Save public file to disk by public key or url