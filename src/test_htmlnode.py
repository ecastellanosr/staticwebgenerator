import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })
        node2 = HTMLNode(
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })
        self.assertEqual(node, node2)

    
    def test_not_eq(self):
        node = HTMLNode(tag = "h1",
                        value = "this is a p",
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })
        node2 = HTMLNode(tag = "p",
                        value = "this is a p",
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })
        self.assertNotEqual(node,node2)
    
    def test_children(self):
        node = HTMLNode(tag = "h1",
                        value = "this is a p",
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })
        node2 = HTMLNode(tag = "h1",
                        value = "this is a h1 tag",)
        node3 = HTMLNode(tag = "p",
                        value = "this is a p",
                        children = [node,node2],
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })    
        self.assertTrue(node3.children)

    def test_props_to_html(self):
        node = HTMLNode(tag = "h1",
                        value = "this is a p",
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })
        node2 = HTMLNode(tag = "h1",
                        value = "this is a h1 tag",)
        node3 = HTMLNode(tag = "p",
                        value = "this is a p",
                        children = [node,node2],
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })    
        self.assertIn('href="https://www.google.com" target="_blank"', node3.props_to_html())
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, wordle!")
        self.assertEqual(node.to_html(), '<h1>Hello, wordle!</h1>')
        
    def test_props_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!",props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                            })
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">Hello, world!</p>')
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(tag="p",value=None)  
        self.assertRaises(ValueError,node.to_html)
    
    def test_to_html_parent_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_parent_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node,child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span></div>")

    def test_to_html_parent_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_parent_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("span", [grandchild_node2])
        parent_node = ParentNode("div", [child_node,child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span><p>grandchild2</p></span></div>",
        )
    def test_to_html_parent_with_grandchildren2(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("p", "grandchild2")
        grandchild_node3 = LeafNode("b", "grandchild3")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("span", [grandchild_node2,grandchild_node3])
        parent_node = ParentNode("div", [child_node,child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span><p>grandchild2</p><b>grandchild3</b></span></div>",
        )
    def test_to_html_parent_with_grandchildren2_inverted(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("p", "grandchild2")
        grandchild_node3 = LeafNode("b", "grandchild3")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("span", [grandchild_node2,grandchild_node3])
        parent_node = ParentNode("div", [child_node2,child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p>grandchild2</p><b>grandchild3</b></span><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_parent_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError,parent_node.to_html)
    
    def test_to_html_parent_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError,parent_node.to_html)
        
    def test_to_html_parent_with_blank_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        self.assertRaises(ValueError,parent_node.to_html)
if __name__ == "__main__":
    unittest.main()