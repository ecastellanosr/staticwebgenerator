from enum import Enum
from htmlnode import ParentNode,LeafNode
from textnode import TextNode, TextType
from nodes_delimiter import split_nodes_delimiter, combine_same_type_nodes
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    striped_list = list(map(lambda x: x.strip(),markdown.split("\n")))
    markdown = "\n".join(striped_list)
    markdowns = markdown.split("\n\n")
    markdowns = list(map(lambda x: x.strip(),markdowns))
    for block in markdowns:
        if block == "":
            markdowns.remove(block)
            
    return markdowns
        
def block_to_block_type(block):
    if block[0] == "#":
        return BlockType.HEADING
    elif block[:3] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        return BlockType.QUOTE
    elif block[0] == "-":
        return BlockType.UNORDERED_LIST
    elif block[:2] == "1.":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    code_block_counter = 0
    for block in blocks:
        htmlnode = block_to_html_node(block)
        if block_to_block_type(block) == BlockType.CODE:
            code_block_counter += 1
            htmlnode = code_block_to_html_node(block,markdown,code_block_counter)
        children_nodes.append(htmlnode)
    return ParentNode("div",children_nodes,None)
        
        
        
def block_to_html_node(block):
    if block_to_block_type(block) == BlockType.CODE:
        return ""

    
    elif block_to_block_type(block) == BlockType.HEADING:
        counter = 0
        for letter in block[:6]:
            if letter == "#":
                counter += 1
        childrenNodes = text_to_children(block[counter:].lstrip(),BlockType.HEADING)
        return ParentNode(f"h{counter}",childrenNodes,None)
    
    elif block_to_block_type(block) == BlockType.ORDERED_LIST:
        childrenNodes = text_to_children(block,BlockType.ORDERED_LIST)
        return ParentNode("ol",childrenNodes,None)
    
    elif block_to_block_type(block) == BlockType.UNORDERED_LIST:
        childrenNodes = text_to_children(block,BlockType.UNORDERED_LIST)
        return ParentNode("ul",childrenNodes,None)
    
    elif block_to_block_type(block) == BlockType.QUOTE:
        
        childrenNodes = text_to_children(block,BlockType.QUOTE)
        return ParentNode("blockquote",childrenNodes,None)
    else:
        childrenNodes = text_to_children(block,BlockType.PARAGRAPH)
        return ParentNode("p",childrenNodes,None)
    
def code_block_to_html_node(block,markdown,counter):
    allcodes = re.findall(r'```([^`]*)```',markdown)
    codeText = allcodes[counter-1]
    codeNode = LeafNode(None,codeText.strip())
    # codeNode = LeafNode(None,block[3:-3].lstrip())
    return ParentNode("pre",[ParentNode("code",[codeNode])])

def text_to_children(block,blocktype):
    children = []
    lines = block.split("\n")
    if blocktype == BlockType.ORDERED_LIST or blocktype == BlockType.UNORDERED_LIST:
        for line in lines:
            line = line.split(' ', 1)[1]
            nodes = split_nodes_delimiter(TextNode(line,TextType.TEXT))
            line_children = nodes_to_html(nodes)
            list_item = ParentNode("li",line_children)
            children.append(list_item)
        return children
    elif blocktype == BlockType.QUOTE:
        for line in lines:
            if len(line.strip()) == 1:
                continue
            line = line.split(' ', 1)[1]
            nodes = split_nodes_delimiter(TextNode(line,TextType.TEXT))
            children += nodes
        
        new_children = combine_same_type_nodes(children)
        html_children = nodes_to_html(new_children)
        return html_children
    
    for line in lines:
        nodes = split_nodes_delimiter(TextNode(line,TextType.TEXT))
        children += nodes
       
    new_children = combine_same_type_nodes(children)   
    html_children = nodes_to_html(new_children)

    return html_children 
    
        
def nodes_to_html(nodes):
    children = []
    for node in nodes:
        leaf = node.text_node_to_html_node()
        children.append(leaf)
    return children
            