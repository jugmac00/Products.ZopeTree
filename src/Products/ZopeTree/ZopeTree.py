#
# ZopeTree
#
# Simple tree implementation for Zope
#
# Copyright (c) 2001-2003 by Philipp "philiKON" von Weitershausen
#
# This software is distributed under the terms of the Mozilla Public
# License (MPL)
#

"""
$Id: ZopeTree.py,v 1.8 2003/05/30 15:13:02 philipp Exp $
"""

import zlib

import zope.interface
from ZTUtils.Tree import a2b, b2a

from Products.ZopeTree.IZopeTree import INode, IZopeTree


@zope.interface.implementer(INode)
class Node:

    __allow_access_to_unprotected_subobjects__ = 1

    def _get_attr(self, attr):
        """
        Get the attribute 'attr' from the wrapped object. If the
        result is callable, call it.
        """
        attr = getattr(self.object, attr)
        if callable(attr):
            return attr()
        else:
            return attr

    def _create_children_nodes(self):
        """
        Create children nodes
        """
        try:
            children = self._get_attr(self._children_attr)
        # yes, this is bad, but _get_attr can throw almost all exceptions
        except:  # noqa
            self._children_nodes = []
            return
        nodes = []
        for obj in children:
            node = Node(
                obj,
                self.depth + 1,
                self._id_attr,
                self._children_attr,
                self._expanded_nodes,
            )
            nodes.append(node)
        self._children_nodes = nodes

    def __init__(self, object, depth, id_attr, children_attr, expanded_nodes=[]):
        # attributes required by the interface
        self.object = object
        self.depth = depth
        self.expanded = 0

        self._id_attr = id_attr
        self._children_attr = children_attr
        self._expanded_nodes = expanded_nodes

        if self.getId() in expanded_nodes:
            self.expand()

    def expand(self, recursive=0):
        self.expanded = 1
        if recursive:
            for node in self.getChildrenNodes():
                node.expand(1)

    def collapse(self):
        self.expanded = 0

    def getId(self):
        return self._get_attr(self._id_attr)

    def hasChildren(self):
        try:
            return len(self._get_attr(self._children_attr)) > 0
        except AttributeError:
            return 0

    def getChildrenNodes(self):
        if not self.expanded:
            return []
        # children nodes are not created until they are explicitly requested
        # through this function
        if not hasattr(self, "_children_nodes"):
            self._create_children_nodes()
        return self._children_nodes[:]

    def getFlatNodes(self):
        nodes = []
        for node in self.getChildrenNodes():
            nodes.append(node)
            nodes += node.getFlatNodes()
        return nodes


def safe_decompress(input, max_size=10240):
    # this sillyness can go away in python 2.2
    decomp = zlib.decompressobj()
    output = ""
    while input:
        fragment_size = max(1, (max_size - len(output)) / 1000)
        fragment, input = input[:fragment_size], input[fragment_size:]
        output += decomp.decompress(fragment)
        if len(output) > max_size:
            raise ValueError("Compressed input too large")
    return output + decomp.flush()


@zope.interface.implementer(IZopeTree)
class ZopeTree(Node):

    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(
        self,
        root_object,
        id_attr="getId",
        children_attr="objectValues",
        request=None,
        request_variable="tree-expansion",
        expanded_nodes=[],
        set_cookie=1,
    ):
        tree_expansion = request.get(request_variable, "")
        if tree_expansion:
            if set_cookie:
                # set a cookie right away
                request.RESPONSE.setCookie(request_variable, tree_expansion)
            expanded_nodes = self.decodeTreeExpansion(tree_expansion)

        super().__init__(root_object, 0, id_attr, children_attr, expanded_nodes)
        self.expand()

    def encodeTreeExpansion(self, expanded_nodes):
        tree_expansion = ":".join(expanded_nodes)
        if not isinstance(tree_expansion, bytes):
            tree_expansion = tree_expansion.encode("utf-8")
        tree_expansion = zlib.compress(tree_expansion)
        return b2a(tree_expansion)

    def decodeTreeExpansion(self, tree_expansion):
        tree_expansion = a2b(tree_expansion)
        tree_expansion = zlib.decompress(tree_expansion)
        if not isinstance(tree_expansion, str):
            tree_expansion = tree_expansion.decode("utf-8")
        return tree_expansion.split(":")

    def getFlatDicts(self):
        flatdicts = []
        self.maxdepth = 0
        for node in self.getFlatNodes():
            id = node.getId()
            expanded_nodes = self._expanded_nodes[:]
            if id in self._expanded_nodes:
                # if the node is already expanded, the next step is
                # collapsing it
                expanded_nodes.remove(id)
            else:
                # if it isn't, the next step is expanding it.
                expanded_nodes += [id]
            flatdicts.append(
                {
                    "id": id,
                    "expanded": node.expanded,
                    "depth": node.depth,
                    "children": node.hasChildren(),
                    "tree-expansion": self.encodeTreeExpansion(expanded_nodes),
                    "object": node.object,
                }
            )
            if node.depth > self.maxdepth:
                self.maxdepth = node.depth
        return flatdicts
