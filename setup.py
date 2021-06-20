#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-cmc",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_cmc"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-cmc=tap_cmc:main
    """,
    packages=["tap_cmc"],
    package_data = {
        "schemas": ["tap_cmc/schemas/*.json"]
    },
    include_package_data=True,
)
