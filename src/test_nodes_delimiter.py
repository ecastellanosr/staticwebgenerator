import unittest

from textnode import TextNode, TextType
from nodes_delimiter import split_nodes_delimiter, extract_markdown_image, extract_markdown_link

class Test_Bold_italic_code_Delimiter(unittest.TestCase):
    def test_text_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
    def test_text_italic(self):
        node = TextNode("This is text with a _italics block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italics block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ])
        
    def test_text_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ])
        
    def test_bold_italic(self):
        node = TextNode("This is text with a **bold block** word", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.ITALIC),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.ITALIC),
            ])

    def test_text_bold_and_italic(self):
        node = TextNode("This is text with a **bold block** word and a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
            ])
        
    def test_text_code_and_italic(self):
        node = TextNode("This is text with a `code block` word and a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
            ])

    def test_text_code_and_code(self):
        node = TextNode("This is text with a `code block` word and a `second code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("second code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ])

    def test_text_code_and_code_asterisk(self):
        node = TextNode("This is text with a `code block` word and a `second code block` word and an asterisk *", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("second code block", TextType.CODE),
            TextNode(" word and an asterisk *", TextType.TEXT)
            ])

    def test_text_bold_and_italic_nested(self):
        node = TextNode("This is text with a **bold block word with a _italic nested block_ word** and an asterisk *", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block word with a ", TextType.BOLD),
            TextNode("italic nested block", TextType.ITALIC),
            TextNode(" word", TextType.BOLD),
            TextNode(" and an asterisk *", TextType.TEXT)
            ])
class Test_Images_Links_Delimiter(unittest.TestCase):    
    def test_extract_images(self):
        matching_text = "![image](https://i.imgur.com/zjjcJKZ.png)"
        match, length = extract_markdown_image(matching_text)
        self.assertEqual(TextNode("image",TextType.IMAGE,"https://i.imgur.com/zjjcJKZ.png"),match) and self.assertEqual(len(matching_text),length)
    
    def test_extract_images2(self):
        text = "![second image](https://i.imgur.com/3elNhQu.png) what a great image!"
        matching_text = "![second image](https://i.imgur.com/3elNhQu.png)"
        match, length = extract_markdown_image(text)
        self.assertEqual(TextNode("second image",TextType.IMAGE,"https://i.imgur.com/3elNhQu.png"),match) and self.assertEqual(len(matching_text),length)
    
    def test_extract_link(self):
        text = "[to boot dev](https://www.boot.dev) what the helly?!"
        matching_text = "[to boot dev](https://www.boot.dev)"
        match, length = extract_markdown_link(text)
        self.assertEqual(TextNode("to boot dev",TextType.LINK,"https://www.boot.dev"),match) and self.assertEqual(len(matching_text),length)
     
    def test_extract_no_images(self):
        text = "![what???] what a great image!"
        match, length = extract_markdown_image(text)
        self.assertEqual(None,match) and self.assertEqual(0,length)
    
    def test_extract_no_link(self):
        text = "[question] what the helly?!"
        match, length = extract_markdown_link(text)
        self.assertEqual(None,match) and self.assertEqual(0,length)
    
    def test_text_code_and_link(self):
        node = TextNode("This is text with a `code block` word and a link [to boot dev](https://www.boot.dev) what the helly?!", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK,"https://www.boot.dev"),
            TextNode(" what the helly?!", TextType.TEXT)
            ])

    def test_text_code_and_image(self):
        node = TextNode("This is text with a `code block` word and an image ![image](https://i.imgur.com/zjjcJKZ.png) what the helly?!", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and an image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE,"https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" what the helly?!", TextType.TEXT)
            ])
        
    def test_text_with_braces(self):
        node = TextNode("This is text with [braces] word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with [braces] word", TextType.TEXT),
            ])
        
    def test_text_with_excalamtion_braces(self):
        node = TextNode("This is text with ![braces] word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with ![braces] word", TextType.TEXT),
            ])
class Test_all_delimiters(unittest.TestCase):
    def test_all_delimiters(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ])
    def test_no_delimiters(self):
        node = TextNode("This is * with an _ word and a ` and an ![ and a [", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node)
        self.assertEqual(new_nodes, [
            TextNode("This is * with an _ word and a ` and an ![ and a [", TextType.TEXT),
            ])
    
if __name__ == "__main__":
    unittest.main()
