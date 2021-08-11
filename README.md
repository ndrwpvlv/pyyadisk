# PyYaDisk
**PyYaDisk** is a wrapper over Yandex Disk Rest API V1. 
The library is in creation process. You can check realized features with our roadmap below. 

## Usage
```python
from pyyadisk import YandexDisk

token = 'ya_oauth_token'
disk = YandexDisk(token=token)  # Make instance
print(disk.path('yandex/disk/path').get())  # Get path info
disk.path('old/yandex/disk/path').move('new/yandex/disk/path')  # Move by path
disk.path('old/yandex/disk/path').copy('new/yandex/disk/path')  # Copy by path
disk.path('yandex/disk/new_path').create()  # Make directory
disk.path('yandex/disk/path').create('new_path')  # Make directory in directory
disk.path('yandex/disk/path').delete()  # Delete directory
print(disk.path('yandex/disk/path').link())  # Get private link
print(disk.path('yandex/disk/path').share())  # Share path and get public link
disk.path('yandex/disk/path').unshare()  # Unshare path
print(disk.last_uploaded())  # Get last uploaded files info
print(disk.list_files())  # Get files list info
disk.path('yandex/disk/path').upload('/home/file.pdf')  # Upload file
disk.path('yandex/disk/path').upload_by_url('file.pdf', 'https://example.com/file.pdf')  # Upload file by url
```

## Roadmap
- [x] OAuth authorization by token

`/v1/disk`
- [x] Get disk metadata

`/v1/disk/resources`
- [x] Get metadata of file or directory
- [x] Create directory
- [x] Delete of file or directory
- [x] Move of file or directory
- [x] Copy of file or directory
- [x] Get download link (private)
- [x] Share directory or file and get public link
- [ ] Get download link (public)
- [x] Get list of files
- [x] Get last uploaded files
- [x] Upload file
- [x] Upload file by url

`/v1/disk/resources/save-to-disk`
- [ ] Save public file to disk by public key or url