from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, props)
        self.children = children if isinstance(children, list) else [children]
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag cannot be None")
        if self.children == None:
            raise ValueError("Children cannot be None")
        text_props = super().props_to_html()
        html_string = f"<{self.tag}{text_props}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string
    
    # def __repr__(self):
    #     return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"