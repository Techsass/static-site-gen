import sys
from textnode import *
from filehelpers import *

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    # proj_path = "/mnt/c/Users/gnart/code/github/techsass/boot/static-gen/static-site-gen"

    copy_contents(f"{basepath}static", f"{basepath}docs")
    generate_pages_recursive(f"{basepath}content", f"{basepath}template.html", f"{basepath}docs", f"{basepath}")

main()