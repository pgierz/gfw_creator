#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=6.0",
    "xarray",
    "cdo",
    "netcdf4",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
]

setup(
    author="Paul Gierz",
    author_email="pgierz@awi.de",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    description="GFW Creator allows you to generate files for the gfw_atmo switch in ECHAM6/JSBACH of AWI-ESM",
    entry_points={
        "console_scripts": ["gfw_creator=gfw_creator.cli:main",],
        "esm_tools.plugins": [
            "create_hosing_files=gfw_creator.esm_tools_plugin:create_hosing_files",
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="gfw_creator",
    name="gfw_creator",
    packages=find_packages(include=["gfw_creator"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/pgierz/gfw_creator",
    version="0.2.2",
    zip_safe=False,
)
