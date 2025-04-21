#!/usr/bin/env python3
"""
Setup script for offline-transcriber package.
"""

import os
from setuptools import setup, find_packages

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Read version from __init__.py
with open(os.path.join(this_directory, "src", "offline_transcriber", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split('=')[1].strip().strip('"').strip("'")
            break

setup(
    name="offline-transcriber",
    version=version,
    description="CLI tool for offline audio transcription using Whisper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hussein Daoud",
    author_email="lhussein.daoud@gmail.com",
    url="https://github.com/hussein-da/offline-transcriber",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pydub>=0.25.1",
        "openai-whisper>=20230314",
        "tqdm>=4.64.0",
    ],
    entry_points={
        "console_scripts": [
            "transcribe=offline_transcriber.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Utilities",
    ],
    keywords="transcription, speech-to-text, whisper, audio, cli",
    license="MIT",
    project_urls={
        "Source": "https://github.com/hussein-da/offline-transcriber",
        "Bug Reports": "https://github.com/hussein-da/offline-transcriber/issues",
    },
) 