from setuptools import find_packages, setup

setup(
    name="Products.ZopeTree",
    version="2.0.2.dev0",
    url="https://github.com/jugmac00/Products.ZopeTree",
    project_urls={
        "Issue Tracker": "https://github.com/jugmac00/Products.ZopeTree/issues",
        "Sources": "https://github.com/jugmac00/Products.ZopeTree",
    },
    description="ZopeTree is a light-weight tree implementation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
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
