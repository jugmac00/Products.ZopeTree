#
# ZopeTree
#
# Copyright (c) 2001-2003 by Philipp "philiKON" von Weitershausen
#
# This software is distributed under the terms of the Mozilla Public License
# (MPL)
#

from zope.interface import Interface
from AccessControl import allow_module

__allow_access_to_unprotected_subobjects__ = 1
__roles__ = None

# make ZopeTree module accessible from PythonScript and ZPT
from Products.ZopeTree.ZopeTree import ZopeTree, Node
from Products.ZopeTree.TreeObjectWrapper import TreeObjectWrapper
allow_module('Products.ZopeTree')
