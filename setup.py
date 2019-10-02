from setuptools import setup, find_packages

setup(
    name='basic',
    version='0.0.1',
    packages=find_packages('basic'),
    install_requires=[
        'Parsley>=1.3',
    ],
)
