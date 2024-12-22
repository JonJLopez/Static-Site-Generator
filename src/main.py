from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inlinesplit import split_nodes_delimiter
from extract_links import extract_markdown_images

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.web.com")
    htmlnode = HTMLNode("h1", "text inside")
    leafnode = LeafNode("p", "text")
    parentnode = ParentNode(None, [LeafNode("p", "text", {"key": "site"})],)

    node = TextNode("code block", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    print(new_nodes)


main()