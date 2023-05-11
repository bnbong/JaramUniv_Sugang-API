"""
setting up packages to make sure our machine read our packages properly.
"""
from os import path

from setuptools import setup, find_packages

working_dir = path.abspath(path.dirname(__file__))

if __name__ in ("__main__", "builtins"):
    setup(
        name="jaramhub-sugangAPI",
        description="FastAPI sugang shinchung API",
        url="https://github.com/bnbong/JaramUniv_Sugang-API",
        author="bnbong",
        author_email="bbbong9@gmail.com",
        packages=find_packages(),
        package_data={},
        python_requires=">=3.10, <3.11"
    )
