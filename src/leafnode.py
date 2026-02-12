from htmlnode import HTMLNode
from textnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Value cannot be None")
        if self.tag == None:
            return self.value
        text_props = super().props_to_html()
        return f"<{self.tag}{text_props}>{self.value}</{self.tag}>"