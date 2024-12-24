from inlinesplit import *
from htmlnode import *
from textnode import *

def extract_title(markdown):
    blocks = markdown_to_block(markdown)
    for block in blocks:
        if block_to_block_type(block) == "h1":
            return block[2:].strip()
    raise ValueError("No title found")
