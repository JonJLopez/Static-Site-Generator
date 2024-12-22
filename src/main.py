from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.web.com")
    htmlnode = HTMLNode("h1", "text inside")
    leafnode = LeafNode("p", "text")
    parentnode = ParentNode(None, [LeafNode("p", "text", {"key": "site"})],)
    print(parentnode.to_html())


main()