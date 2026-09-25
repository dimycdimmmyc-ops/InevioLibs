from setuptools import setup, find_packages

setup(
    name='inevio-mycelium',
    version='1.0.0',
    description='Living mycelium for Inevio: search, attach, penetrate deeper',
    long_description=(
        'Inevio Mycelium — sixth package of the Inevio ecosystem.\n\n'
        'Grows through the network layer by layer:\n'
        '- SCOUT: find new neighbors via all channels\n'
        '- ATTACH: connect and remember\n'
        '- PENETRATE: go deeper through gateways\n'
        '- ASSESS: decide where to grow next\n'
        '- TEACH: share knowledge with other mycelia\n'
        '- MERGE: combine maps with other organisms\n'
    ),
    long_description_content_type='text/markdown',
    author='Inevio',
    packages=find_packages(include=['inevio_mycelium', 'inevio_mycelium.*']),
    python_requires='>=3.8',
    install_requires=[
        'spore-net>=1.2.0',
        'spore-bridge>=1.0.0',
    ],
)