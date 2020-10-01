#
# TreeObjectWrapper
#
# Copyright (c) 2001-2003 by Philipp "philiKON" von Weitershausen
#
# This software is distributed under the terms of the Mozilla Public
# License (MPL)
#

"""
$Id: TreeObjectWrapper.py,v 1.5 2003/04/30 10:01:55 philipp Exp $
"""

import posixpath


class TreeObjectWrapper:
    """
    A wrapper around Zope objects to be more flexible when displaying
    them with ZopeTree.

    Extend this class with methods filtering the return list of
    getChildren() to your own needs.
    """

    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, obj, path=""):
        self.path = path
        self.object = obj
        self.id = obj.getId()
        self.folderish = obj.isPrincipiaFolderish

    def getChildren(self):
        if not self.folderish:
            return []
        children = []
        objectIds = self.object.objectIds()
        objectIds.sort()
        for id in objectIds:
            path = posixpath.join(self.path, id)
            obj = getattr(self.object, id)
            children.append(TreeObjectWrapper(obj, path))
        return children

    def getFolderishChildren(self):
        return [child for child in self.getChildren() if child.folderish]
