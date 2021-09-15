#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='hydra-pywr-common',
    version='0.4',
    description='Common data types and functions for Hydra and pywr integration.',
    packages=find_packages(include=['hydra_pywr_common', 'hydra_pywr_common.*', 'hydra_pywr_common.lib', 'hydra_pywr_common.lib.*']),
    include_package_data=True,
)
