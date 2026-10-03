from setuptools import setup, find_packages

setup(
    name='inevio-mycorizanet',
    version='1.0.0',
    description='МИКОРИЗАnet — overlay-организм с автономным выбором транспорта',
    packages=find_packages(include=['inevio_mycorizanet', 'inevio_mycorizanet.*']),
    python_requires='>=3.8',
    install_requires=[],
)