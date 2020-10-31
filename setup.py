"""Setup for SSACC package."""

from pathlib import Path

import setuptools

project_dir = Path(__file__).parent


setuptools.setup(
    name="ssacc",
    version="0.1.0",
    description="Map ZIPs to SSA County Code",
    extras_require=dict(tests=["pytest"]),
    packages=setuptools.find_packages(where="ssacc"),
    package_dir={"": "ssacc"},
    license="MIT",
    license_files=["LICENSE.txt"],
)
