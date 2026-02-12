import re
import string
from leafnode import *
from textnode import * 

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("No valid text type detected")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextType.LINK:
        prop = {"href": text_node.url}
        return LeafNode(tag="a", value=text_node.text, props=prop)
    if text_node.text_type == TextType.IMAGE:
        prop = {"src": text_node.url, "alt": text_node.text}
        return LeafNode(tag="img", value="", props=prop)
    
def reorder_nodes(string, nodes):
    new_order = nodes
    for node in nodes:
        if string.startswith(node.text):
            new_order.remove(node)
            new_order.insert(0, node)
        if string.endswith(node.text):
            new_order.remove(node)
            new_order.insert(len(nodes), node)
    return new_order

def split_punctuation(text):
    split = []
    punc = ".,\"!:"
    for punc_char in punc:
        if text.endswith(punc_char):
            word = text.split(punc_char)[0]
            punc_split = [word]
            punc_split.append(punc_char)
            split.extend(punc_split)
        if text.startswith(punc_char):
            word = text.split(punc_char)[0]
            punc_split = [word]
            punc_split.append(punc_char)
            split.extend(punc_split)
    if split != []:
        return split
    else:
        return text

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    all_new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            all_new_nodes.append(old_node)
            continue
        first_split = old_node.text.split(" ")
        split = []
        for item in first_split:
            if delimiter in item:
                punc_split = split_punctuation(item)
                if punc_split != item:
                    split.extend(punc_split)
                else:
                    split.append(item)
            else:
                split.append(item)
        start_index = None
        end_index = None
        styled_items = []
        for index, item in enumerate(split):
            if item.startswith(delimiter) and item.endswith(delimiter):
                styled_items.append((index, index))
            else:
                if item.startswith(delimiter):
                    start_index = index
                if item.endswith(delimiter):
                    styled_items.append((start_index, index))
                    start_index = None
        if styled_items == []:
            all_new_nodes.append(old_node)
        if start_index != None and styled_items == []:
            raise Exception("No closing delimiter found, unable to split nodes due to invalid markdown")
        if styled_items != None:
            ordered = []
            node_to_process = old_node
            loop_count = 0
            for styled_item in styled_items:
                loop_count += 1
                new_nodes = []
                start_index = styled_item[0]
                end_index = styled_item[1]
                styled = " ".join(split[start_index:end_index+1])
                nonstyled = node_to_process.text.split(styled)
                item = nonstyled[0]
                if item != "":
                    new_nodes.append(TextNode(item, TextType.TEXT))
                    new_nodes.append(TextNode(styled.strip(delimiter), text_type))
                    print("not_blank", new_nodes)
                if item == "":
                    new_nodes.append(TextNode(styled.strip(delimiter), text_type))
                    new_nodes.append(TextNode(item, TextType.TEXT))
                    print("blank", new_nodes)
                if len(nonstyled) > 1:
                    new_nodes.append(TextNode(nonstyled[-1], TextType.TEXT))
                    print("over", new_nodes)
                if len(styled_items) > 1 and loop_count != len(styled_items):
                    node_to_process = new_nodes[-1]
                    new_nodes.pop()
                print("processing", node_to_process)
                print("new_nodes", new_nodes)
                ordered.extend(new_nodes)
                print("ordered", ordered)
            all_new_nodes.extend(ordered)
    return all_new_nodes
        
def extract_markdown_images(text):
    image = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image

def extract_markdown_links(text):
    link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link

def split_nodes_image(old_nodes):
    all_new_nodes = []
    for old_node in old_nodes:
        new_nodes = []
        if old_node.text_type != TextType.TEXT:
            all_new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if images == []:
            all_new_nodes.append(old_node)
            continue
        split = [old_node.text]
        for image in images:
            image_alt = image[0]
            image_link  = image[1]
            split = split[0].split(f"![{image_alt}]({image_link})", 1)
            if split[0] != "":
                text_node = TextNode(split[0], TextType.TEXT)
                new_nodes.append(text_node)
            split.pop(0)
            image_node = TextNode(image_alt, TextType.IMAGE, image_link)
            new_nodes.append(image_node)
        for residual in split:
            if residual != "":
                residual_text_node = TextNode(residual, TextType.TEXT)
                new_nodes.append(residual_text_node)
    all_new_nodes.extend(new_nodes)
    return all_new_nodes

def split_nodes_link(old_nodes):
    all_new_nodes = []
    for old_node in old_nodes:
        new_nodes = []
        if old_node.text_type != TextType.TEXT:
            all_new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if links == []:
            all_new_nodes.append(old_node)
            continue
        split = [old_node.text]
        for link in links:
            link_alt = link[0]
            link  = link[1]
            split = split[0].split(f"[{link_alt}]({link})", 1)
            if split[0] != "":
                text_node = TextNode(split[0], TextType.TEXT)
                new_nodes.append(text_node)
            split.pop(0)
            link_node = TextNode(link_alt, TextType.LINK, link)
            new_nodes.append(link_node)
        for residual in split:
            if residual != "":
                residual_text_node = TextNode(residual, TextType.TEXT)
                new_nodes.append(residual_text_node)
    all_new_nodes.extend(new_nodes)
    return all_new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    bold = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    images = split_nodes_image(code)
    links = split_nodes_link(images)
    return links