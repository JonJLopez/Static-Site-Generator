import unittest
from htmlnode import *
from textnode import *
from inlinesplit import *
from markdown import *

class TestMarkdown(unittest.TestCase):
    def test_extract_title_no_title(self):
        with self.assertRaises(ValueError):
            markdown = "this has not markdown"
            extract_title(markdown)

    def test_extract_title(self):
        markdown = "# title"
        correct = "title"
        self.assertEqual(correct, extract_title(markdown))
