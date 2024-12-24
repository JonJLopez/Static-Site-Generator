from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inlinesplit import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_children
from extract_links import extract_markdown_images
import os
import shutil

def copy_source_to_destination(src, dest):
    paths_in_src = os.listdir(src)
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)
    for path in paths_in_src:
        src_path = os.path.join(src, path)
        print(f"currently copying {src_path} to {dest}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest)
        else:
            new_dest = os.path.join(dest, path)
            copy_source_to_destination(src_path, new_dest)
        


def main():
    copy_source_to_destination("static", "public")

main()