#!/usr/bin/env python
import os.path

import os
from distutils.core import setup

with open(os.path.join("requirements", "server.txt"), encoding="utf-8") as reqs:
    REQUIREMENTS = [reqs.readlines()]

setup(
    name="Open-Needs Server",
    version="1.0",
    description="Open-Needs Server",
    author="Open-Needs community",
    url="https://www.open-needs.org",
    packages=["open_needs_server"],
    python_requires=">=3.10",
    install_requires=REQUIREMENTS,
    entry_points={"console_scripts": ["ons = open_needs_server.main:start"]},
)
