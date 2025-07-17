class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return None
        fstring = ""
        for prop in self.props:
            fstring += f'{prop}="{self.props[prop]}" '
        return fstring.rstrip()
    
    def __repr__(self):
        string = ""
        if self.tag != None:
            string += f'tag = {self.tag}\n'
        if self.value != None:
            string += f'value = {self.value}\n'
        if self.children != None:
            string += f'children = {self.children}\n'
        if self.props != None:
            string += f'props = {self.props_to_html()}\n'
        return string.rstrip()
    
    def __eq__(self,other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag=tag,value=value,props=props)
 
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode's value is required")
        elif self.tag == None or self.tag == "":
            return self.value
        
        string = f'<{self.tag}>{self.value}</{self.tag}>'
        if self.props != None:
            string = f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
        return string
    
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,children=children,props=props)
 
    def to_html(self):
        if not self.children:
            raise ValueError("ParentNode's children is missing")
        elif self.tag == None or self.tag == "":
            raise ValueError("ParentNode needs a tag value")
        
        start_parent_string = f'<{self.tag}>'
        if self.props != None:
            start_parent_string = f'<{self.tag} {self.props_to_html()}>'
        
        end_parent_string = f'</{self.tag}>' 
        for child in self.children:
            child_string = child.to_html()
            start_parent_string += child_string
        
        return start_parent_string + end_parent_string
        
        