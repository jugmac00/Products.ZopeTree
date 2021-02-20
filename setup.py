import codecs
import os

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = "3.2.0"


def read(*parts):
    """Build an absolute path from *parts*...

    ... and return the contents of the resulting file.
    Assume UTF-8 encoding.

    Thanks to:
    https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


setup(
    name="Products.ZopeTree",
    version=VERSION,
    url="https://github.com/jugmac00/Products.ZopeTree",
    project_urls={
        "Issue Tracker": "https://github.com/jugmac00/Products.ZopeTree/issues",
        "Sources": "https://github.com/jugmac00/Products.ZopeTree",
    },
    description="ZopeTree is a light-weight tree implementation.",
    long_description=read("README.rst") + "\n\n" + read("CHANGES.rst"),
    long_description_content_type="text/x-rst",
    author="Philipp von Weitershausen",
    author_email="philipp@weitershausen.de",
    maintainer="Juergen Gmach",
    maintainer_email="juergen.gmach@googlemail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Zope :: 4",
        "Framework :: Zope :: 5",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages("src"),
    namespace_packages=["Products"],
    package_dir={"": "src"},
    python_requires=">3.5",
    install_requires=[
        "Zope",
        "setuptools",
        "AccessControl",
        "zope.interface",
        "zope.testing",
    ],
    extras_require={
        "test": [
            "pytest >=6.1.1",
            "pytest-cov",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
