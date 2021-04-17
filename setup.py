# Adapted from https://packaging.python.org/tutorials/packaging-projects/
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tufted_twitmouse",
    version="0.1.0",
    author="bwmabe",
    author_email="benwmabe@gmail.com",
    description="An asynchronous Twitter watcher/follower",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bwmabe/tufted-twitmouse",
    project_urls={
        "Bug Tracker": "https://github.com/bwmabe/tufted-twitmouse/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
