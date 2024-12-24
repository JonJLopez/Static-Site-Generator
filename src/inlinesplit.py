from textnode import TextType, TextNode, text_node_to_html_node
from extract_links import extract_markdown_images, extract_markdown_links
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        # If node has proper markdown syntax, there should always be n*2 delimiters in text
        # This would result in a new split list of an odd number of elements.
        # Otherwise of it is an even number of elements, there was no matching delimiter
        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax no matching {delimiter}")
        #tracks if current text in split_text is of TypeText.TEXT or not (if not, would be text_type passed as param)
        is_text = True
        for text in split_text:
            if is_text and text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
            if not is_text:
                new_nodes.append(TextNode(text, text_type))
            is_text = not is_text
        
    return new_nodes
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        section = old_node.text
        images = extract_markdown_images(section)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            sections = section.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_link))
            # we don't have to worry about the string before the current link being added to new node list
            section = sections[1]
        if section != "":
            new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        section = old_node.text
        links = extract_markdown_links(section)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = section.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINKS, link_url))
            section = sections[1]
        if section != "":
            new_nodes.append(TextNode(section, TextType.TEXT))    
    return new_nodes

def text_to_textnodes(text):
    starting_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([starting_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    return split_nodes_link(new_nodes)

def markdown_to_block(markdown):
    # returns a list of strings split into "blocks" from text
    # blocks are seperated by an empty line
    blocks = map(lambda x: x.strip(" \n"), markdown.split("\n\n"))
    return list(filter(lambda x: x != "", blocks))

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ")):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if len(list(filter(lambda x: x.startswith(">"), lines))) == len(lines):
        return "blockquote"
    if len(list(filter(lambda x: x.startswith("* ") or x.startswith("- "), lines))) == len (lines):
        return "ul"
    i = 1
    for line in lines:
        if line.startswith(f"{i}. "):
            i += 1
            continue
        break
    if i - 1 == len(lines):
        return "ol"
    return "p"

def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    htmlnodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "blockquote":
                text = " ".join(map(lambda x: x[1:], block.split("\n")))
                htmlnodes.append(ParentNode("blockquote", text_to_children(text)))
            case "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
                htmlnodes.append(ParentNode(block_type, text_to_children(block[2:])))
            case "ul":
                list_items = []
                for list_item in block.split("\n"):
                    list_items.append(ParentNode("li", text_to_children(list_item[2:])))
                htmlnodes.append(ParentNode(block_type, list_items))
            case "ol":
                list_items = []
                for list_item in block.split("\n"):
                    list_items.append(ParentNode("li", text_to_children(list_item[3:])))
                htmlnodes.append(ParentNode(block_type, list_items))
            case "code":
                code_node = LeafNode("code", block[3:-3])
                htmlnodes.append(ParentNode("pre", [code_node]))
            case "p":
                htmlnodes.append(ParentNode("p", text_to_children(block)))

    parentnode = ParentNode("div", htmlnodes)
    return parentnode

def text_to_children(text):
    children_nodes = []
    textnodes = text_to_textnodes(text)
    for text_node in textnodes:
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes