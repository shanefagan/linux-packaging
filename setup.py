import datetime
import glob
import os

import setuptools
from setuptools import setup

version = datetime.datetime.now().strftime("%Y%m%d")
with open("VERSION", "w") as version_file:
    version_file.write(version)

requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
else:
    requirements = []

setup(
    name="packaging-demo",
    maintainer="Shane Fagan",
    maintainer_email="mail@example.com",
    version=version,
    packages=setuptools.find_packages(),
    scripts=glob.glob("bin/*.py"),
    python_requires=">3.6",
    install_requires=requirements,
)
