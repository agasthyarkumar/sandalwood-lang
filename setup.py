from setuptools import find_packages, setup


setup(
    name="sandalwood-lang",
    version="0.1.0",
    description="Sandalwood interpreted programming language foundations",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    python_requires=">=3.10",
)
