from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inlinesplit import split_nodes_delimiter, split_nodes_image, split_nodes_link
from extract_links import extract_markdown_images

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.web.com")
    htmlnode = HTMLNode("h1", "text inside")
    leafnode = LeafNode("p", "text")
    parentnode = ParentNode(None, [LeafNode("p", "text", {"key": "site"})],)

    node = TextNode("code block", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    node_link_image = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    link_split = split_nodes_link([node_link_image])
    print(link_split)
    print(split_nodes_image(link_split))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    print(node_link_image)


main()