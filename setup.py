#!/usr/bin/env python3
"""
gdlcli - Google Drive Loader
A fast, lightweight Python package for downloading any file from Google Drive.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="gdlcli",
    version="1.0.0",
    author="mfaeezshabbir",
    author_email="mfaeezshabbir@gmail.com",
    description="A fast, lightweight Python package for downloading any file from Google Drive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mfaeezshabbir/gdlcli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ]
    },
    entry_points={
        "console_scripts": [
            "gdlcli=gdlcli.cli:main",
        ],
    },
    keywords="google-drive download file-downloader cli api",
    project_urls={
        "Bug Reports": "https://github.com/mfaeezshabbir/gdlcli/issues",
        "Source": "https://github.com/mfaeezshabbir/gdlcli",
        "Documentation": "https://github.com/mfaeezshabbir/gdlcli#readme",
    },
)
