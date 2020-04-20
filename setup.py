import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gindex",
    version="0.0.1a1", # a-alpha b-beta rc-release candidate
    author="Tal Soikis",
    author_email="talsoikis@gmail.com",
    description="A pure python geometrical indexing library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # TODO insert later
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6", # TODO change this thing and add license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)