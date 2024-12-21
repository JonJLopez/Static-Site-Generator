import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()