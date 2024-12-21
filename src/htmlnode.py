from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # string representing HTML tag name
        self.value = value          # string representing value of HTML tag
        self.children = children    # list of HTMLNode objects representing children of this node
        self.props = props          # dictionary representing attributes of HTML tag

    def __repr__(self):
        return (f"--------HTMLNODE--------\n"
        + f"tag = {self.tag}\n"
        + f"value = {self.value}\n"
        + f"children = {self.children}\n"
        + f"props = {self.props}")
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return reduce(lambda out, key: out + f' {key}="{self.props[key]}"', self.props, "") 