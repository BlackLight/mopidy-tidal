from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall('__([a-z]+)__ = "([^"]+)"', fh.read()))
        return metadata["version"]


setup(
    name="Mopidy-Tidal",
    version=get_version("mopidy_tidal/__init__.py"),
    url="https://github.com/tehkillerbee/mopidy-tidal",
    license="Apache License, Version 2.0",
    author="Johannes Linde",
    author_email="josaksel.dk@gmail.com",
    description="Tidal music service integration",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "setuptools",
        "Mopidy >= 3.0",
        "Pykka >= 1.1",
        "tidalapi @ git+https://github.com/BlackLight/python-tidal",
        "requests >= 2.0.0",
    ],
    entry_points={
        "mopidy.ext": [
            "tidal = mopidy_tidal:Extension",
        ],
    },
    classifiers=[
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Sound/Audio :: Players",
    ],
)
