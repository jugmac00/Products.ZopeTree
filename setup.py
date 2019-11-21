from setuptools import setup, find_packages

setup(name='Products.ZopeTree',
      version='2.0.dev',
      url='https://github.com/jugmac00/Products.ZopeTree',
      license='MPL 1.1',
      description="ZopeTree is a light-weight tree implementation.",
      author='Philipp von Weitershausen and Contributors',
      long_description="ZopeTree is a light-weight tree implementation.",
      packages=find_packages('src'),
      namespace_packages=['Products'],
      package_dir={'': 'src'},
      install_requires=[
        'setuptools',
        'six',
        'AccessControl',
        'Zope',
        'zope.interface',
        'zope.testing',
      ],
      include_package_data=True,
      zip_safe=False,
      )