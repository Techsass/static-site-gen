import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        prop_dict = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        node = LeafNode(tag="a", value="test value dood", props=prop_dict)
        converted = node.to_html()
        expected = "<a href=\"https://www.google.com\" target=\"_blank\">test value dood</a>"
        self.assertEqual(converted, expected)


if __name__ == "__main__":
    unittest.main()