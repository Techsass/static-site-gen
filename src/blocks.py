import re
from blockhelpers import *
from enum import Enum
from htmlnode import *
from parentnode import *
from leafnode import *
from nodehelpers import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    split = markdown.split("\n\n")
    final_list = []
    for block in split:
        block = block.strip()
        block_to_add = block
        if block == "":
            continue
        if "\n" in block:
            split_block = block.split("\n")
            block_list = []
            for line in split_block:
                if line == "":
                    continue
                block_list.append(line)
            block_to_add =  "\n".join(block_list)
        final_list.append(block_to_add)
    return final_list

def block_to_block_type(block):
    block_split = block.split(r"\n")
    heading_match = re.search(r"^\#{1,6}", block)
    code_match_start =  re.search(r"^```", block)
    code_match_end =  re.search(r"```$", block)
    quote_match = re.search(r"^>", block, re.M)
    unordered_match = re.search(r"^-[ ]", block, re.M)
    ordered_match = re.search(r"^\d*\.", block, re.M)
    line_count = 1
    for line in block_split:
        if line.startswith(str(line_count)):
            ordered_match = True
            line_count += 1
        else:
            ordered_match = None
            break
    if heading_match:
        return BlockType.HEADING
    if code_match_start and code_match_end:
        return BlockType.CODE
    if quote_match:
        return BlockType.QUOTE
    if unordered_match:
        return BlockType.UNORDERED_LIST
    if ordered_match:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        block_nodes.append(block_node)
    div_node = ParentNode("div", block_nodes)
    return div_node

def heading_count(heading):
    count = 0
    for char in heading:
        if count > 6:
            return 6
        if char == "#":
            count += 1
        else:
            return count
        
def extract_title(markdown):
    split = markdown.split('\n')
    for line in split:
        line = line.lstrip()
        title = re.search(r"^\#{1}\s\b.*$", line)
        if title:
            stripped = title.group().lstrip("# ")
            return stripped
        else:
            continue
    if not title:
        raise Exception("No title found in the markdown provided")
 
def block_to_html_node(block, block_type):
    new_line_split = block.split("\n")
    children = []
    if block_type != BlockType.CODE:
        for item in new_line_split:
            item = strip_md_chars(item)
            children.append(text_to_children(item))
    if block_type == BlockType.HEADING:
        count = heading_count(block)
        block_node = ParentNode(f"h{count}", children[0], None)
    if block_type == BlockType.CODE:
        inner_node = text_node_to_html_node(TextNode(block.strip("```").lstrip("\n"), TextType.CODE))
        block_node = ParentNode("pre", inner_node, None)
    if block_type == BlockType.QUOTE:
        quote_node_list = []
        for child in children:
            for node in child:
                quote_node_list.append(node) 
        block_node = ParentNode("blockquote", quote_node_list, None)
    if block_type == BlockType.UNORDERED_LIST:
        li_node_list = []
        for child in children:
            li_node_list.append(ParentNode("li", child, None))                
        block_node = ParentNode("ul", li_node_list, None)
    if block_type == BlockType.ORDERED_LIST:
        li_node_list = []
        for child in children:
            li_node_list.append(ParentNode("li", child, None))  
        block_node = ParentNode("ol", li_node_list, None)
    if block_type == BlockType.PARAGRAPH:
        block_node = ParentNode("p", children[0], None)
    return block_node

def strip_md_chars(text):
    #strip chars before making HTML node
    heading_match = re.search(r"^\#{1,6}\s", text)
    quote_match = re.search(r"^>\s", text, re.M)
    quote_match_empty = re.search(r">", text, re.M)
    unordered_match = re.search(r"^-[ ]", text, re.M)
    ordered_match = re.search(r"^\d*\.\s", text, re.M)
    if heading_match != None:
        text = text.lstrip(heading_match.group())
    if quote_match != None:
        text = text.lstrip(quote_match.group())
    if quote_match_empty != None:
        text = text.lstrip(quote_match_empty.group())
    if unordered_match != None:
        text = text.lstrip(unordered_match.group())
    if ordered_match != None:
        text = text.lstrip(ordered_match.group())
    return text
    
def text_to_children(text):
    nodes = text_to_textnodes(text)
    child_html_nodes = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        child_html_nodes.append(html_node)
    return child_html_nodes