from textnode import TextType, TextNode

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
            raise Exception(f"Invalid markdown syntax no matching {delimiter}")
        #tracks if current text in split_text is of TypeText.TEXT or not (if not, would be text_type passed as param)
        is_text = True
        for text in split_text:
            if is_text and text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
            if not is_text:
                new_nodes.append(TextNode(text, text_type))
            is_text = not is_text
        
    return new_nodes
        