# PyYADisk
**PyYADisk** is a wrapper over Yandex Disk Rest API V1. 
The library is in creation process. You can check realized features with our roadmap below. 

# Usage
```python
from pyyadisk import YandexDisk

token = 'ya_oauth_token'
disk = YandexDisk(token=token)  # Make instance
print(disk.path('your_path').get())  # Get path info
disk.path('old_path').move('new_path')  # Move by path
disk.path('old_path').copy('new_path')  # Copy by path
disk.path('path').create()  # Make directory
disk.path('path').create('subdirectory')  # Make directory in directory
disk.path('path').delete()  # Delete directory
print(disk.path('path').link())  # Get private link
print(disk.path('path').share())  # Share path and get public link
disk.path('path').unshare()  # Unshare path
print(disk.last_uploaded())  # Get last uploaded files info
print(disk.list_files())  # Get files list info
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
- [x] Share directory or file
- [x] Get download link (public)
- [x] Get list of files
- [x] Get last uploaded files

