import unittest
from htmlnode import HTMLNode, LeafNode

class testHTMLNode(unittest.TestCase):
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

class testLeafNode(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()