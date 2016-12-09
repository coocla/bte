#coding:utf-8
from setuptools import setup, find_packages


setup(
    name="bte",
    version="1.0",
    scripts=[
        "bin/bte_api",
    ],
    packages=find_packages(),
    data_files=[
        ('/etc/bte/', ['etc/config', 'etc/black.json', 'etc/white.json']),
        ('/etc/rsyslog.d/', ['etc/lion.conf'])
    ]
)
