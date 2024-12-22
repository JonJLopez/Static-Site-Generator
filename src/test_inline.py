import unittest
from inlinesplit import split_nodes_delimiter
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

    
if __name__ == "__main__":
    unittest.main()