from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # string representing HTML tag name
        self.value = value          # string representing value of HTML tag
        self.children = children    # list of HTMLNode objects representing children of this node
        self.props = props          # dictionary representing attributes of HTML tag

    def __repr__(self):
        return (f"tag: {self.tag}, "
        + f"value: {self.value}, "
        + f"children: {self.children}, "
        + f"props: {self.props}")
    
    def __eq__(self, other):
        return (self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props)
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return reduce(lambda out, key: out + f' {key}="{self.props[key]}"', self.props, "") 

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("Parent node must have a tag value")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent node must have children")
        return f"<{self.tag}{self.props_to_html()}>{reduce(lambda text, node: text + node.to_html(), self.children, '')}</{self.tag}>"