from pathlib import Path

from setuptools import setup

setup(
    name="uplink-httpx",
    version="1.4",
    description="HttpX Client for Uplink",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Christian Assing",
    author_email="chris@ca-net.org",
    url="https://github.com/chassing/uplink-httpx",
    packages=["uplink_httpx"],
    install_requires=Path("requirements.txt").open().readlines(),
    license="MIT License, Copyright (c) 2019 Christian Assing",
    platforms="any",
    keywords=["uplink", "httpx", "asyncio", "rest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
