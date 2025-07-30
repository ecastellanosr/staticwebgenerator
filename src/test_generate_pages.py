import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from generate_pages import extract_title


class Testextract_titles(unittest.TestCase):
     def test_headings(self):
        md = """
        # this is an h1

        this is paragraph text

        ## this is an h2
        """

        title = extract_title(md)
        self.assertEqual(
            title,
            "this is an h1",
        )