import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "text inside", ["child1", "child2", "child3"], {"href":"www.site.com", "target":"_blank"})
        correct = ' href="www.site.com" target="_blank"'
        self.assertEqual(node.props_to_html(), correct)

    def test_prop_to_html_None(self):
        node = HTMLNode("h1", "text inside", ["child1", "child2", "child3"])
        correct = ''
        self.assertEqual(node.props_to_html(), correct)

    def test_prop_to_html_empty(self):
        node = HTMLNode("h1", "text inside", ["child1", "child2", "child3"], {})
        correct = ''
        self.assertEqual(node.props_to_html(), correct)
    def test_eq(self):
        node = HTMLNode("t", "text", ["item1", "item2"], {"a": "1", "b": "2"})
        node2 = HTMLNode("t", "text", ["item1", "item2"], {"a": "1", "b": "2"})
        self.assertEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        correct = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), correct)

    def test_to_html_props_empty(self):
        node = LeafNode("p", "This is a paragraph of text.")
        correct = '<p>This is a paragraph of text.</p>'
        self.assertEqual(node.to_html(), correct)

    def test_to_html_props_None(self):
        node = LeafNode("p", "This is a paragraph of text.", None)
        correct = '<p>This is a paragraph of text.</p>'
        self.assertEqual(node.to_html(), correct)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Text")
        correct = "Text"
        self.assertEqual(node.to_html(), correct)

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            html = node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_parent_leaf_no_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        correct = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), correct)

    def test_to_html_parent_leaf_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", {"href": "https://www.google.com"}),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href":"www.site.com", "target":"_blank"}
        )
        correct = '<p href="www.site.com" target="_blank"><b href="https://www.google.com">Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), correct)

    def test_to_html_parent_leaf_props_empty(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", ""),
                LeafNode(None, "Normal text", ""),
                LeafNode("i", "italic text", ""),
                LeafNode(None, "Normal text", ""),
            ],
            ""
        )
        correct = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), correct)

    def test_to_html_nested_parent_no_props(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "b", 
                    [
                    LeafNode(None, "Normal text", ""),
                    LeafNode("i", "italic text", ""),
                    ],
                ),
                LeafNode(None, "Normal text", ""),
            ],
        )
        correct = '<p><b>Normal text<i>italic text</i></b>Normal text</p>'
        self.assertEqual(node.to_html(), correct)

    def test_to_html_many_nested_parent(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("i", "italic nested text"),
                                LeafNode("b", "bold nested text"),
                            ],
                        ),
                    ],
                ),
            ],
        )
        correct = '<p><p><p><i>italic nested text</i><b>bold nested text</b></p></p></p>'
        self.assertEqual(node.to_html(), correct)
    
    def test_to_html_many_nested_parent_prop(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("i", "italic nested text", ),
                                LeafNode("b", "bold nested text", {"href": "https://www.google.com"}),
                            ],
                        ),
                    ],
                    {"href": "https://www.google.com"}
                ),
            ],
        )
        correct = '<p><p href="https://www.google.com"><p><i>italic nested text</i><b href="https://www.google.com">bold nested text</b></p></p></p>'
        self.assertEqual(node.to_html(), correct)
    
    def test_to_html_parent_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", [], "")
            node.to_html()
    
    def test_to_html_nested_parent_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                "p", 
                [
                    ParentNode("b", [],)
                ], 
                ""
            )
            node.to_html()

    def test_to_html_tag_None(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("p", "Text")], {"href": "site"})
            node.to_html()

    def test_to_html_tag_empty(self):
        with self.assertRaises(ValueError):
            node = ParentNode("", [LeafNode("p", "Text")], {"href": "site"})
            node.to_html()

    def test_to_html_nested_parents_with_leaf_each(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    [LeafNode("t", "first", {"href": "site"})],
                ),
                ParentNode(
                    "i",
                    [LeafNode("t", "second")],
                ),
            ],
        )
        correct = '<p><b><t href="site">first</t></b><i><t>second</t></i></p>'
        self.assertEqual(node.to_html(), correct)
if __name__ == "__main__":
    unittest.main()