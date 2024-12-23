import unittest
from inlinesplit import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestInlineSplit(unittest.TestCase):
    def test_inline(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct)

    def test_inline_delimiter_at_front(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct)

    def test_inline_no_split(self):
        node = TextNode("Text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("Text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct)

    def test_inline_no_split_ending_whitespace(self):
        node = TextNode("Text    ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("Text    ", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct)
    
    def test_inline_multiple_splits(self):
        node = TextNode("This is text with a `code` `block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct)       

    def test_inline_multiple_splits_no_whitespace(self):
        node = TextNode("This is text with a `code``block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct)       
    
    def test_inline_multiple_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is just text `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        correct = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is just text ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(new_nodes, correct)
    def test_inline_multiple_nodes_and_text_types(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is just text *italics*", TextType.TEXT)
        code_split = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        italic_split = split_nodes_delimiter(code_split, "*", TextType.ITALIC)
        correct = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is just text ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC)
        ]
        self.assertEqual(italic_split, correct)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        correct = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
                ),
        ]
        self.assertEqual(correct, split_nodes_link([node]))
    
    def test_split_nodes_links_multiple_nodes(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        correct = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(correct, split_nodes_link([node , node2]))
    
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        correct = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGES, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
                ),
        ]
        self.assertEqual(correct, split_nodes_image([node]))

    def test_split_nodes_images_multiple_nodes(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        correct = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGES, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGES, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(correct, split_nodes_image([node, node2]))  

    def test_split_nodes_image_and_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        correct = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        link_split = split_nodes_link([node])
        self.assertEqual(correct, split_nodes_image(link_split))

    def test_split_nodes_image_only_text(self):
        node = TextNode(
            "This is text ",
            TextType.TEXT,
        )
        correct = [node]
        self.assertEqual(correct, split_nodes_image([node]))
    
    def test_split_nodes_link_only_text(self):
        node = TextNode(
            "This is text ",
            TextType.TEXT,
        )
        correct = [node]
        self.assertEqual(correct, split_nodes_link([node]))
if __name__ == "__main__":
    unittest.main()