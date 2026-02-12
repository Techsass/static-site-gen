import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_full(self):
        node = TextNode("Test text", TextType.CODE, "https://techsass.site")
        node2 = TextNode("Text test", TextType.IMAGE, "https://techsass.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Test text", TextType.CODE, "https://techsass.site")
        node2 = TextNode("Test text", TextType.CODE, "https://techsass.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Test text", TextType.CODE, "https://techsass.site")
        node2 = TextNode("Text test", TextType.CODE, "https://techsass.site")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("Test text", TextType.CODE, "https://techsass.site")
        node2 = TextNode("Test text", TextType.BOLD, "https://techsass.site")
        self.assertNotEqual(node, node2)
    


if __name__ == "__main__":
    unittest.main()