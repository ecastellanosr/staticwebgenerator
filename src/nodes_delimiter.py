from textnode import TextType, TextNode
from stack import MarkStack
import re

markdown_list = [
    "*",
    "_",
    "`",
    "!",
    "["
]

def split_nodes_delimiter(node):
    new_nodes = []
    value = node.text
    i = 0
    text_type = node.text_type
    marks = MarkStack(text_type)
    marks.push(text_type)
    current_text = ""
    text_length = len(value)
    
    while i < text_length:
        if value[i] not in markdown_list:
            current_text += value[i]
            i += 1
        elif i == text_length-1:
            if marks.peek() == text_type:
                current_text += value[i]
            i += 1
        
        #Bold
        elif value[i] == "*" and value[i+1] == "*":
            if marks.peek() == TextType.BOLD:
                new_nodes.append(TextNode(current_text,marks.pop()))
                current_text = ""
                i += 2
            else:
                new_nodes.append(TextNode(current_text,marks.peek()))
                marks.push(TextType.BOLD)
                current_text = "" 
                i +=2
        
        #italics
        elif value[i] == "_":
            if marks.peek() == TextType.ITALIC:
                new_nodes.append(TextNode(current_text,marks.pop()))
                current_text = ""
                i += 1
            elif not value[i+1] == " ":
                new_nodes.append(TextNode(current_text,marks.peek()))
                #reset
                marks.push(TextType.ITALIC)
                current_text = "" 
                i +=1
            else:
                current_text += value[i]
                i += 1
        
        #code
        elif value[i] == "`":
            if marks.peek() == TextType.CODE:
                new_nodes.append(TextNode(current_text,marks.pop()))
                current_text = ""
                i += 1
            elif not value[i+1] == " ":
                new_nodes.append(TextNode(current_text,marks.peek()))
                #reset
                marks.push(TextType.CODE)
                current_text = "" 
                i +=1
            else:
                current_text += value[i]
                i += 1
        
        #images
        elif value[i] == "!" and value[i+1] == "[":
            image_node, length = extract_markdown_image(value[i:])
            if image_node is not None:
                new_nodes.append(TextNode(current_text,marks.pop()))
                current_text = ""
                new_nodes.append(image_node)
                i += length
            else:
                current_text += value[i] + value[i+1]
                i += 2    
        
        #links
        elif value[i] == "[":
            link_node, length = extract_markdown_link(value[i:])
            if link_node is not None:
                new_nodes.append(TextNode(current_text,marks.pop()))
                current_text = ""
                new_nodes.append(link_node)
                i += length
            else:
                current_text += value[i]
                i += 1
        else:
            current_text += value[i]
            i += 1  
    if current_text != " " and current_text != "" and current_text != None:
        new_nodes.append(TextNode(current_text,marks.pop()))
    return new_nodes

def extract_markdown_image(text):
    name_link = re.match(r"!\[(.*?)\]\((.*?)\)",text)
    if name_link == None:
        return None,0
    length = name_link.span(0)[1]
    image = TextNode(name_link.group(1),TextType.IMAGE,name_link.group(2))
    return image, length

def extract_markdown_link(text):
    name_link = re.match(r"\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    if name_link == None:
        return None,0
    length = name_link.span(0)[1]
    link = TextNode(name_link.group(1),TextType.LINK,name_link.group(2))
    return link, length

def combine_same_type_nodes(nodes):
    new_nodes = []
    i = 0
    last_type = None
    while i < len(nodes):
        if last_type == nodes[i].text_type:
            new_text = new_nodes[-1].text + nodes[i].text
            new_nodes[-1] = TextNode(new_text,nodes[i].text_type)
            i += 1
        elif (nodes[i].text_type == TextType.IMAGE or 
            nodes[i].text_type == TextType.IMAGE or 
            nodes[i].text_type != nodes[i+1].text_type):
            
            new_nodes.append(nodes[i],nodes[i+1])
            last_type = nodes[i+1].text_type
            i += 2
        
        else:
            new_text = nodes[i].text + nodes[i+1].text
            new_nodes.append(TextNode(new_text,nodes[i].text_type))
            last_type = nodes[i].text_type
            i += 2
    return new_nodes