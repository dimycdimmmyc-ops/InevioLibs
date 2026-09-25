from setuptools import setup, find_packages

setup(
    name='spore-bridge',
    version='1.0.0',
    description='Мост между InevioLibs и spore-net',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['spore-net>=1.2.0'],
)