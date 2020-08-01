from setuptools import find_packages, setup
from pathlib import Path


project_dir = Path(__file__).parent

setuptools.setup(
    name="ssacc",
    version="0.1.0",
    description="Map ZIPs to SSA County Code",
    extras_require=dict(tests=["pytest"]),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="MIT",
    license_files=["LICENSE.txt"],
)
