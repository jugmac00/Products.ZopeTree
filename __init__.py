#
# ZopeTree
#
# Copyright (c) 2001-2003 by Philipp "philiKON" von Weitershausen
#
# This software is distributed under the terms of the Mozilla Public License
# (MPL)
#

"""
$Id: __init__.py,v 1.3 2003/03/13 08:34:38 philipp Exp $
"""

# make sure, 'from Interface import Interface' will work...
try:
    from Interface import Interface
except ImportError:
    # Zope <2.6
    import Interface
    Interface.Interface = Interface.Base

__allow_access_to_unprotected_subobjects__ = 1
__roles__ = None

# make ZopeTree module accessible from PythonScript and ZPT
from AccessControl import allow_module
from ZopeTree import ZopeTree
from TreeObjectWrapper import TreeObjectWrapper
allow_module('Products.ZopeTree')
