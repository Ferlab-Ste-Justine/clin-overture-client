import json
from setuptools import setup, find_packages

with open('info.json', 'r') as info_file:
    INFO = json.load(info_file)

setup(
    name=INFO['name'],
    version=INFO['version'],
    packages=find_packages(),
    install_requires=[
        'Click==7.0',
        'docker==4.2.0',
        'marshmallow==3.5.0'
    ],
    entry_points='''
        [console_scripts]
        overturecli=overturecli:cli
    ''',
)