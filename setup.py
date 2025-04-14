"""
Setup script for RecruitReach2.

This script provides a setuptools-based setup script for the RecruitReach2 package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="RecruitReach2",
    version="1.0.0",
    author="Ravi Ahuja",
    author_email="raviahuja1998@gmail.com",
    description="AI-powered application for generating personalized recruiter outreach emails and cover letters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RecruitReach2",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "recruitreach=RecruitReach2.main:main",
        ],
    },
    include_package_data=True,
)
