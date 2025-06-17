from setuptools import setup, find_packages

setup(
    name="synchmanlib",
    version="0.2.2",
    description="Shared utilities for the SynchMan synchronization and device management system",
    author="K-Mart",
    url="https://github.com/Jitzwaz/SynchManLib",
    packages=find_packages(),
    install_requires=[
        "requests",
        "cryptography"
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)