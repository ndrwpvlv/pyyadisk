import re
import requests


def join_path(uri, resource_path):
    return '{}{}'.format(uri, resource_path) if resource_path else uri


def filter_dict_by_key(d: dict):
    return {k: v for k, v in d.items() if v}


def download(link):
    try:
        with requests.get(link, stream=True) as response:
            if response.status_code == 200:
                filename = re.findall("filename.*''(.*\.?\w*)", response.headers['content-disposition'])[0]
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
    except Exception as e:
        print(e)
        filename = None
    return filename
