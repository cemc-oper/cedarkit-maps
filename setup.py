from setuptools import setup, find_packages
import codecs
from os import path
import io
import re

with io.open("meda/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

here = path.abspath(path.dirname(__file__))

with codecs.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='meda',

    version=version,

    description='A graph tool for NWP.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/perillaroc/meda',

    author='perillaroc',
    author_email='perillaroc@gmail.com',

    license='GPLv3',

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],

    keywords='graphic',

    packages=find_packages(exclude=['docs', 'tests', 'example']),

    include_package_data=True,

    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "cartopy",
        "xarray",
    ],

    extras_require={
        "test": ['pytest'],
        "cov": ['pytest-cov', 'codecov']
    },
)
