import unittest

from textnode import TextNode, TextType


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
        node = TextNode("This is a text node", TextType.NORMAL, "website")
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


if __name__ == "__main__":
    unittest.main()