#
# ZopeTree
#
# Copyright (c) 2001-2003 by Philipp "philiKON" von Weitershausen
#
# This software is distributed under the terms of the Mozilla Public License
# (MPL)
#

"""
$Id: __init__.py,v 1.5 2003/03/15 17:40:06 philipp Exp $
"""

# make sure, 'from Interface import Interface' will work...
try:
    from Interface import Interface
except ImportError:
    # Zope <2.6
    import Interface
    Interface.Interface = Interface.Base

# make sure 'from AccessControl import allow_module' works...
try:
    from AccessControl import allow_module
except ImportError:
    # Zope <2.5
    import AccessControl
    from AccessControl import ModuleSecurityInfo
    def allow_module(module_name):
        ModuleSecurityInfo(module_name).setDefaultAccess(1)
        dot = module_name.find('.')
        while dot > 0:
            ModuleSecurityInfo(module_name[:dot]).setDefaultAccess(1)
            dot = module_name.find('.', dot + 1)

__allow_access_to_unprotected_subobjects__ = 1
__roles__ = None

# make ZopeTree module accessible from PythonScript and ZPT
from ZopeTree import ZopeTree, Node
from TreeObjectWrapper import TreeObjectWrapper
allow_module('Products.ZopeTree')
