from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inlinesplit import split_nodes_delimiter


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.web.com")
    htmlnode = HTMLNode("h1", "text inside")
    leafnode = LeafNode("p", "text")
    parentnode = ParentNode(None, [LeafNode("p", "text", {"key": "site"})],)

    node = TextNode("code block", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    print(new_nodes)


main()