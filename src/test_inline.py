import unittest
from inlinesplit import (
    split_nodes_delimiter, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes,
    markdown_to_block,
    block_to_block_type,
    markdown_to_html_node
    )
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

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
    
    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        correct = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ]
        self.assertEqual(correct, text_to_textnodes(text))

    def test_text_to_textnode_only_text(self):
        text = "only text"
        correct = [TextNode("only text", TextType.TEXT)]
        self.assertEqual(correct, text_to_textnodes(text))

    def test_text_to_textnode_invalid_syntax(self):
        with self.assertRaises(ValueError):
            text = "text *italic text* more text **invalid bold text"
            nodes = text_to_textnodes(text)
    
    def test_markdown_to_blocks(self):
        markdown = ("# This is a heading\n"
        + "\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
        + "\n* This is the first list item in a list block\n"
        + "* This is a list item\n"
        + "* This is another list item")
        correct = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertListEqual(correct, markdown_to_block(markdown))
    
    def test_markdown_to_blocks_empty(self):
        markdown = ""
        correct = []
        self.assertListEqual(correct, markdown_to_block(markdown))

    def test_markdown_to_blocks_2_empty_lines(self):
        markdown = "line 1\n\n\nline 2"
        correct = ["line 1", "line 2"]
        self.assertListEqual(correct, markdown_to_block(markdown))

    def test_block_to_block_type_heading1(self):
        text = "# heading"
        self.assertEqual(block_to_block_type(text), "h1")

    def test_block_to_block_type_heading2(self):
        text = "## heading"
        self.assertEqual(block_to_block_type(text), "h2")

    def test_block_to_block_type_heading3(self):
        text = "### heading"
        self.assertEqual(block_to_block_type(text), "h3")

    def test_block_to_block_type_heading4(self):
        text = "#### heading"
        self.assertEqual(block_to_block_type(text), "h4")

    def test_block_to_block_type_heading5(self):
        text = "##### heading"
        self.assertEqual(block_to_block_type(text), "h5")

    def test_block_to_block_type_heading6(self):
        text = "###### heading"
        self.assertEqual(block_to_block_type(text), "h6")
    
    def test_block_to_block_type_paragraph(self):
        text = "This is a paragraph"
        self.assertEqual(block_to_block_type(text), "p")

    def test_block_to_block_type_code(self):
        text = "```This is a code block\nmore code\neven more code```"
        self.assertEqual(block_to_block_type(text), "code")

    def test_block_to_block_type_quote(self):
        text = ">quote line 1\n>quote line 2\n> quote line 3"
        self.assertEqual(block_to_block_type(text), "blockquote")

    def test_block_to_block_type_unordered_list(self):
        text = "* item1\n* item2\n* item 3"
        self.assertEqual(block_to_block_type(text), "ul")

    def test_block_to_block_type_ordered_list(self):
        text = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_block_type(text), "ol")
    
    def test_markdown_to_html_node_quote(self):
        markdown = ">This will be a quote with\n>some *italics* in the quote"
        h1node = LeafNode("h1", "header 1")
        correct = (
            "<div>" \
                "<blockquote>"\
                    "This will be a quote with some <i>italics</i> in the quote"\
                "</blockquote>"\
            "</div>"
            )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), correct)

    def test_markdown_to_html_node_h1(self):
        markdown = "# header 1"
        correct = "<div><h1>header 1</h1></div>"
        self.assertEqual(correct, markdown_to_html_node(markdown).to_html())

    def test_markdown_to_html_node_ul(self):
        markdown = "* item 1\n* item 2\n* *italic* item 3"
        correct = (
            "<div>" \
                "<ul>"\
                    "<li>item 1</li>"\
                    "<li>item 2</li>"\
                    "<li><i>italic</i> item 3</li>"\
                "</ul>"\
            "</div>"
            )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), correct)

    def test_markdown_to_html_node_ol(self):
        markdown = "1. item 1\n2. item 2\n3. *italic* item 3"
        correct = (
            "<div>" \
                "<ol>"\
                    "<li>item 1</li>"\
                    "<li>item 2</li>"\
                    "<li><i>italic</i> item 3</li>"\
                "</ol>"\
            "</div>"
            )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), correct)

    def test_markdown_to_html_node_code(self):
        markdown = "```This is a code block```"
        correct = (
            "<div>"\
                "<pre><code>This is a code block</code></pre>"\
            "</div>"
            )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), correct)

    def test_markdown_to_html_node_paragraph(self):
        markdown = "A simple paragraph with some **bold text**"
        correct = (
            "<div>" \
                "<p>"\
                    "A simple paragraph with some "\
                    "<b>bold text</b>"\
                "</p>"\
            "</div>"
            )
        self.assertEqual(markdown_to_html_node(markdown).to_html(), correct)


if __name__ == "__main__":
    unittest.main()