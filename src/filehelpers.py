import os
import shutil
from blocks import *

def copy_contents(source, destination):
    if not os.path.exists(source):
        raise Exception("Source is empty or doesn't exist, unable to copy files to destination folder")
    if not os.path.exists(destination):
        os.makedirs(destination, 0o755)
    
    if os.listdir(destination) != []:
        shutil.rmtree(destination)
    file_log = []
    files_to_copy = os.listdir(source)
    for entry in files_to_copy:
        source_file_path = f"{source}/{entry}"
        dest_file_path = f"{destination}/{entry}"
        if os.path.isfile(source_file_path):
            log = shutil.copy(source_file_path, dest_file_path)
            file_log.append(log)
        else:
            log = copy_contents(source_file_path, dest_file_path)
            file_log.extend(log)
    return file_log

def generate_page(from_path, template_path, dest_path):
    dest_dir = os.path.dirname(dest_path)[0]
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path).read()
    templ_file = open(template_path).read()
    html_string = markdown_to_html_node(md_file).to_html()
    title = extract_title(md_file)
    template_title = templ_file.replace("{{ Title }}", title)
    template_replaced = template_title.replace("{{ Content }}", html_string)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, 0o755)
    
    with open(dest_path, 'w') as new_html:
        new_html.write(template_replaced)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
            dest_dir = os.path.dirname(dest_dir_path)
            stripped_file = os.path.splitext(dest_dir_path)[0]
            dest_file = os.path.join(dest_dir, stripped_file + ".html")
            print(f"Generating page from {dir_path_content} to {dest_dir} using {template_path}")
            md_file = open(dir_path_content).read()
            templ_file = open(template_path).read()
            html_string = markdown_to_html_node(md_file).to_html()
            title = extract_title(md_file)
            template_title = templ_file.replace("{{ Title }}", title)
            template_replaced = template_title.replace("{{ Content }}", html_string)

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, 0o755)
            with open(dest_file, 'w') as new_html:
                new_html.write(template_replaced)
    else:
            ls = os.listdir(dir_path_content)
            for entry in ls:
                new_dest_dir = os.path.join(dest_dir_path, entry)
                new_dir_path = os.path.join(dir_path_content, entry)
                generate_pages_recursive(new_dir_path, template_path, new_dest_dir)
    
        
        


