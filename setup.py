from setuptools import setup, find_packages

setup(
    name='overturecli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Click==7.0',
        'docker==4.2.0',
        'elasticsearch==6.4.0 '
    ],
    entry_points='''
        [console_scripts]
        overturecli=overturecli:cli
    ''',
)