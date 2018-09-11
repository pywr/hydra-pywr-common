#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='hydra-pywr-common',
    version='0.1',
    description='Common data types and functions for Hydra and pywr integration.',
    packages=find_packages(),
    include_package_data=True,
)
