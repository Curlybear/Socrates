from setuptools import setup, find_packages

setup(
    name="Socrates",
    version="1.0",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    url="https://github.com/Curlybear/Socrates",
    license="",
    author="Curlybear",
    author_email="me@curlybear.eu",
    description="A discord bot for the erepublik web browser game",
)
