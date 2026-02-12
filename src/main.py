from textnode import *
from filehelpers import *

def main():
    proj_path = "/mnt/c/Users/gnart/code/github/techsass/boot/static-gen/static-site-gen"
    files = copy_contents(f"{proj_path}/static", f"{proj_path}/public")
    generate_pages_recursive(f"{proj_path}/content", f"{proj_path}/template.html", f"{proj_path}/public")

main()