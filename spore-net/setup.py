from setuptools import setup, find_packages

setup(
    name='spore-net',
    version='1.2.0',
    description='Живая сеть: конвейер + грибница + дыхание',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='SPORE',
    packages=find_packages(include=['spore', 'spore.*']),
    python_requires='>=3.7',
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Communications',
        'Topic :: Internet',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)