#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

setup(
    author="Théo Delemazure",
    author_email='theo.delemazure@dauphine.eu',
    description="Code for the axis rule project",
    license="GNU General Public License v3",
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='axisrules',
    name='axisrules',
    packages=find_packages(include=['axisrules', 'axisrules.*']),
    url='https://github.com/theoDlmz/AxisRules',
    version='0.1.0',
    zip_safe=False,
)
