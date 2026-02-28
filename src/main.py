import sys
from textnode import *
from filehelpers import *

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    # proj_path = "/mnt/c/Users/gnart/code/github/techsass/boot/static-gen/static-site-gen"
    print(basepath)
    copy_contents(f"./static", f"./docs")
    generate_pages_recursive(f"./content", f"./template.html", f"./docs", f"{basepath}/docs/")

main()