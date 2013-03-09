# -*- coding: utf8 -*-

from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import diagnostics


with open("README.rst") as readme:
    with open("CHANGELOG.rst") as changelog:
        long_description = readme.read() + "\n\n" + changelog.read()

with open("LICENSE.rst") as file:
    license = file.read()


setup(
    name="diagnostics",
    version=diagnostics.__version__,
    description="Alternative to Python's module `cgitb` with template inspired by Nette and Django",
    long_description=long_description,
    author="Michal Belica",
    author_email="miso.belica@gmail.com",
    url="https://github.com/miso-belica/diagnostics",
    license=license,
    keywords=["debug", "cgitb", "traceback"],
    tests_require=[
        "nose",
        "coverage",
    ],
    test_suite="tests",
    install_requires=[],
    packages=[
        "diagnostics",
        "diagnostics.models",
        "diagnostics.logging",
        "diagnostics.formatters",
    ],
    package_data={"diagnostics": [
        "templates/*.png",
        "templates/*.css",
        "templates/*.js",
    ]},
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Topic :: Software Development :: Bug Tracking",
        # "Topic :: Software Development :: Debuggers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
    ),
)
