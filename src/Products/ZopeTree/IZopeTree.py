#
# IZopeTree
#
# Interface for Zope trees
#
# Copyright (c) 2001-2003 by Philipp "philiKON" von Weitershausen
#
# This software is distributed under the terms of the Mozilla Public
# License (MPL)
#

from zope.interface import Attribute, Interface


class INode(Interface):

    object = Attribute(
        """
        The object that is being wrapped.
        """
    )

    depth = Attribute(
        """
        The positional depth of this node in the tree.
        """
    )

    expanded = Attribute(
        """
        True if this node is expanded.
        """
    )

    def __init__(object, depth, id_attr, children_attr, expanded_nodes=[]):
        """
        'object' is the object that is being wrapped

        'depth' is the positional depth of the node in the tree

        'id_attr' should point to an attribute/method name of 'object'
        (and all other wrapped objects), giving each object a unique
        id in the tree.

        'children_attr' should point to an attribute/method name of
        'object' containing/resulting object's children.

        'expanded_nodes' is a list containing ids of nodes that are
        expanded from the beginning.
        """

    def expand(recursive=0):
        """
        Expand this node.

        'recursive' can be set to true to expand all children nodes as
        well
        """

    def collapse():
        """
        Collapse this node.
        """

    def getId():
        """
        Return the object's id in the tree.
        """

    def hasChildren():
        """
        Return true if we have children.
        """

    def getChildrenNodes():
        """
        Return a sequence of children nodes if the node is expanded.
        """

    def getFlatNodes():
        """
        Return a flat list of nodes in the tree. Children of expanded
        nodes are shown.
        """


class IZopeTree(INode):
    def __init__(
        root_object,
        id_attr="",
        children_attr="",
        request=None,
        request_variable="",
        expanded_nodes=[],
        set_cookie=1,
    ):
        """
        'root_object' is the root object of the tree.

        'id_attr' and 'children_attr': see docstring for
        Node.__init__().

        'request' is the HTTP request.

        'request_variable' is the name of a request variable that
        contains the tree expansion information.
        """

    def encodeTreeExpansion(expanded_nodes):
        """
        Encode the tree expansion information in 'expanded_nodes'.
        """

    def decodeTreeExpansion(tree_expansion):
        """
        Decode the tree expansion information 'tree_expansion'.
        """

    def getFlatDicts():
        """
        Works like Node.getFlatNodes() except that it does not return
        a list of nodes but a list of dictionaries.
        """
