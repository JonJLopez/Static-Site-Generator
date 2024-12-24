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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_files = os.listdir(dir_path_content)
    print(f"currently generating content from {dir_path_content}")
    for file in content_files:
        src_path = os.path.join(dir_path_content, file)
        new_dest = os.path.join(dest_dir_path, file)
        print(new_dest)
        if os.path.isfile(src_path):
            new_dest = new_dest[:-2] + "html"
            os.makedirs(dest_dir_path, exist_ok=True)
            generate_page(src_path, template_path, new_dest)
        else:
            next_dir = os.path.join(dest_dir_path, file)
            generate_pages_recursive(src_path, template_path, next_dir)