from inlinesplit import *
from markdown import extract_title
import os
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f: markdown = f.read()
    with open(template_path) as f: template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace(" {{ Title }} ", title)
    template = template.replace("        {{ Content }}", html)

    new_file = open(dest_path, "w")
    new_file.write(template)
    new_file.close()