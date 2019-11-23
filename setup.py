from setuptools import setup, find_packages

setup(
    name="E621",
    version="1.0",
    entry_points={"console_scripts": ["E621=src.main:main"]},
    packages=find_packages(),
    license="MIT",
    install_requires=open("requirements.txt").read(),
)
