
CHANGES
=======

v3.3.0
------

  * add support for Python 3.10

v3.2.0
------

  * add Philipp von Weitershausen as the author of this package

v3.1.0
------

  * use gh actions for CI instead of Travis

v3.0.1
------

  * fix MANIFEST.in

v3.0.0
------

  * enable pre-commit hooks

  * drop support for Python versions < 3.6

  * add support for Python 3.9

  * convert documentation from markdown to restructured text

v2.0.1
------

  * fix link to PyPi badge

v2.0 (2019-11-23)
-----------------

  * add tox environment

  * restructure to use a src directory

  * add a Travis configuration

  * make tests run on Python 2.7 and in a Zope 4 environment

  * add a setup.py

  * fix deprecation warnings

  * replace license file format (HTML->txt)

  * add flake8 and apply it

  * add support for Python 3.6, 3.7, 3.8

v1.3.1 (2003-08-21)
-------------------

  * Fixed tree_menu example. Thanks to Andy McKay for the patch.

v1.3 (2003-05-30)
-----------------

  * Setting a cookie with ZopeTree is optional now. Simply pass
    set_cookie=0 to the ZopeTree constructor.

  * Fixed a security hole in the tree state decompressing
    mechanism. Previous versions were vulnerable to a denial of
    service attack using large tree states. Thanks go to Jamie Heilman
    for reporting the bug and Toby Dickenson for providing a fix.

v1.2 (2003-04-30)
-----------------

  * Added optional 'expanded_nodes' argument to ZopeTree constructor.
    Thanks to Jean Jordaan for suggesting this.

  * Changed signature of TreeObjectWrapper constructor. 'path' is an
    optional argument now.

  * Added collapse() method to ZopeTree.Node.

v1.1 (2003-03-17)
-----------------

  * It now works on Zope 2.4.

  * The unit test was not converted from RevisionManager yet. Fixed.

v1.0 (2003-03-14)
-----------------

  * Initial release.
