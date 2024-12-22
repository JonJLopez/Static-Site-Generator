import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node3 = TextNode("This is a text node", TextType.BOLD, "https://www.web.com")
        node4 = TextNode("This is a text node", TextType.BOLD, "https://www.web.com")
        self.assertEqual(node3, node4)

    def test_different_TextType(self):
        node = TextNode("This is a text node", TextType.TEXT, "website")
        node2 = TextNode("This is a text node", TextType.BOLD, "website")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node3 = TextNode("This is a text node", TextType.BOLD, None)
        node4 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node3, node4)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a different text node", TextType.BOLD, None)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "web")
        self.assertNotEqual(node, node2)
    
    def test_TEXT_type_node_to_html_node(self):
        text_node = TextNode("text", TextType.TEXT)
        html_node = LeafNode(None, "text")
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_BOLD_type_node_to_html_node(self):
        text_node = TextNode("text", TextType.BOLD)
        html_node = LeafNode("b", "text")
        self.assertEqual(text_node_to_html_node(text_node), html_node)
    
    def test_ITALIC_type_node_to_html_node(self):
        text_node = TextNode("text", TextType.ITALIC)
        html_node = LeafNode("i", "text")
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_CODE_type_node_to_html_node(self):
        text_node = TextNode("text", TextType.CODE)
        html_node = LeafNode("code", "text")
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_LINKS_type_node_to_html_node(self):
        text_node = TextNode("text", TextType.LINKS, "www.site.com")
        html_node = LeafNode("a", "text", {"href":"www.site.com"})
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_IMAGES_type_node_to_html_node(self):
        text_node = TextNode("text", TextType.IMAGES, "www.url.com")
        html_node = LeafNode("img", "", {"src": "www.url.com", "alt": "text"})
        self.assertEqual(text_node_to_html_node(text_node), html_node)
    
    def test_text_type_node_to_html_node_invalid_type(self):
        with self.assertRaises(Exception):
            text_node = TextNode("text", "normal text")
            html_node = LeafNode(None, "text")
            self.assertEqual(text_node_to_html_node(text_node), html_node)
        
if __name__ == "__main__":
    unittest.main()