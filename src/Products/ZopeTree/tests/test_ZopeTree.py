"""Test suite."""
import unittest
import zlib
from io import BytesIO

from Testing import ZopeTestCase
from ZPublisher.HTTPRequest import HTTPRequest
from ZPublisher.HTTPResponse import HTTPResponse
from ZTUtils.Tree import b2a

from Products.ZopeTree import Node, ZopeTree
from Products.ZopeTree.IZopeTree import INode, IZopeTree

ZopeTestCase.installProduct("ZopeTree")


# simple object that can have an id and a set of children
class Item:
    def __init__(self, id, children=[]):
        self.id = id
        self.children = children


# function used to convert a set of nested tuples to items and
# children items.
def make_item_from_tuple(item_tuple, dict):
    children = []
    if len(item_tuple) > 1:
        for child in item_tuple[1]:
            children.append(make_item_from_tuple(child, dict))
    item = Item(item_tuple[0], children)
    dict[item_tuple[0]] = item
    return item


tree = ("a", [("b", [("d",), ("e",)]), ("c", [("f", [("h",), ("i",)]), ("g")])])


expanded_nodes = ["a", "c"]


class NodeTest(ZopeTestCase.ZopeTestCase):
    def afterSetUp(self):
        # this mapping will provide shortcuts to each object
        self.items = {}
        self.root_obj = make_item_from_tuple(tree, self.items)
        self.root_node = Node(self.root_obj, 0, "id", "children", expanded_nodes)

    def afterClear(self):
        pass

    def test_verify_interface(self):
        """Verify interface implementation"""
        from zope.interface.verify import verifyObject

        self.assertTrue(verifyObject(INode, self.root_node))

    def test_expand_collapse(self):
        """Test node expansion/collapsion"""
        root_node = self.root_node
        # first the node is expanded
        self.assertTrue(root_node.expanded)
        # now collapse it
        root_node.collapse()
        self.assertFalse(root_node.expanded)
        # make sure there are no children nodes returned!
        self.assertEqual(root_node.getChildrenNodes(), [])
        # expand it again
        root_node.expand()
        self.assertTrue(root_node.expanded)

    def test_children(self):
        """Test children"""
        root_node = self.root_node
        # testing hasChildren()
        self.assertTrue(root_node.hasChildren())

        # testing getChildrenNodes()
        children = [node.object for node in root_node.getChildrenNodes()]
        expected = [self.items["b"], self.items["c"]]
        self.assertEqual(children, expected)

    def test_flat(self):
        """Test flat list generation"""
        root_node = self.root_node
        # testing getFlatNodes()
        children = [node.object for node in root_node.getFlatNodes()]
        # 'a' is not expected because the node on which getFlatNodes()
        # is called is not in the list
        expected = [self.items[i] for i in "bcfg"]
        self.assertEqual(children, expected)


class ZopeTreeTest(ZopeTestCase.ZopeTestCase):
    def afterSetUp(self):
        environ = {"SERVER_NAME": "", "SERVER_PORT": "0"}
        response = HTTPResponse(stdout=BytesIO())
        request = HTTPRequest(BytesIO(), environ, response)
        self.varname = "tree-expansion"
        # emulate a cookie
        tree_expansion = ":".join(expanded_nodes).encode("utf-8")
        request.other[self.varname] = b2a(zlib.compress(tree_expansion))
        self.request = request
        self.items = {}
        self.root_obj = make_item_from_tuple(tree, self.items)
        self.tree = ZopeTree(self.root_obj, "id", "children", request, self.varname)

    def afterClear(self):
        pass

    def test_verify_interface(self):
        """Verify interface implementation"""
        from zope.interface.verify import verifyObject

        self.assertTrue(verifyObject(IZopeTree, self.tree))

    def test_encode_tree_expansion(self):
        """Test tree expansion encoding and decoding"""
        encoded = self.tree.encodeTreeExpansion(expanded_nodes)
        decoded = self.tree.decodeTreeExpansion(encoded)
        self.assertEqual(expanded_nodes, decoded)

    def test_pre_expanded(self):
        """Test pre-expanded nodes"""
        # 'a' is not expected because the node on which getFlatNodes()
        # is called is not in the list
        expected = [self.items[i] for i in "bcfg"]
        # test against to getFlatNodes()
        flat = [node.object for node in self.tree.getFlatNodes()]
        self.assertEqual(flat, expected)

    def test_flat_dicts(self):
        """Test flat dicts"""
        flatdicts = self.tree.getFlatDicts()
        self.assertEqual(len(flatdicts), len(self.tree.getFlatNodes()))
        bdict = flatdicts[0]
        self.assertEqual(bdict["id"], "b")
        self.assertFalse(bdict["expanded"])
        self.assertEqual(bdict["depth"], 1)
        self.assertTrue(bdict["children"])
        self.assertTrue(bdict["object"] is self.items["b"])

    def test_cookie(self):
        """Test cookies"""
        # by default, the tree sets a cookie, so test for that
        request = self.request
        response = request.RESPONSE
        self.assertTrue(self.varname in response.cookies)

        # now make a tree that doesn't set a cookie
        treeexp = response.cookies[self.varname]["value"]
        environ = {"SERVER_NAME": "", "SERVER_PORT": "0"}
        response = HTTPResponse(stdout=BytesIO())
        request = HTTPRequest(BytesIO(), environ, response)
        request.other[self.varname] = treeexp
        self.tree = ZopeTree(
            self.root_obj, "id", "children", request, self.varname, set_cookie=0
        )
        self.assertFalse(self.varname in response.cookies)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NodeTest))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ZopeTreeTest))
    return suite
