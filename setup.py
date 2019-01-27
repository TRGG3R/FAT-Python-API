from setuptools import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Security',
    'Topic :: Security :: Cryptography',
    'Topic :: Software Development',
    'Topic :: System :: Monitoring',
]


setup(
    author="Nolan Bauer",
    author_email="nolan@vbif.io",
    name="fat-python-api",
    version='0.0.1',
    description="Python client library for Factom Asset Tokens",
    long_description=long_description,
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'requests>=2.18.4',
    ],
    url='https://github.com/TRGG3R/FAT-Python-API',
    download_url='https://github.com/bhomnick/factom-api/tarball/0.0.1',
)