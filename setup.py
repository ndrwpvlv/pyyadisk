# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyyadisk',
    version='0.1.2',
    packages=['pyyadisk', ],
    url='https://github.com/ndrwpvlv/pyyadisk',
    license='MIT',
    author='Andrei S. Pavlov',
    author_email='andy_pavlov@outlook.com',
    description='PyYaDisk is a small wrapper over Yandex Disk Rest API V1',
    download_url='https://github.com/ndrwpvlv/pyyadisk/archive/refs/tags/0.1.2.tar.gz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['Yandex', 'Yandex Disk', 'Yandex Disk REST API'],

    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],

    install_requires=['requests == 2.26.0', ],
)
