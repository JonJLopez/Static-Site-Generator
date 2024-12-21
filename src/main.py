from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.web.com")
    htmlnode = HTMLNode("h1", "text inside")
    print(htmlnode)

main()