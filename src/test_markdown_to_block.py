import unittest

from markdown_to_block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class Test_markdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
            )
#same example with a lot of whitespaces
    def test_markdown_to_blocks2(self):
        md = """
       This is **bolded** paragraph      
            
       This is another paragraph with _italic_ text and `code` here   
         This is the same paragraph on a new line    
   
     - This is a list   
    - with items   
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
            )
        
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class Test_BlockType(unittest.TestCase):
    def test_paragraph(self):
        block = """This is **bolded** paragraph"""
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.PARAGRAPH
            )
    def test_unordered_list(self):
        block = """- This is a list
        - with items"""
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.UNORDERED_LIST
            )
        
    def test_heading(self):
        block = """### This is **bolded** heading"""
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.HEADING
            )
        
    def test_code(self):
        block = """```print(x)
        print("Hello world")```"""
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.CODE
            )
        
    def test_quote(self):
        block = """>This is a quote
        >second part of the quote"""
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.QUOTE
            )
        
    def test_ordered_list(self):
        block = """1.banana
        2.apple
        3.UK"""
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.ORDERED_LIST
            )

class Test_Markdown_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here
        
        This is another paragraph with _italic_ text and `code` here
        """
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
        
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )