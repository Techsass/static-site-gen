import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        converted = node.props_to_html()
        expected = ""
        self.assertEqual(converted, expected)

    def test_props_to_html_multi_value(self):
        prop_dict = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        node = HTMLNode(tag="a", props=prop_dict)
        converted = node.props_to_html()
        expected = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(converted, expected)

    def test_props_to_html_single_value(self):
        prop_dict = {
            "src": "/shared/audio/test.mp3",
            }
        node = HTMLNode(tag="audio", props=prop_dict)
        converted = node.props_to_html()
        expected = " src=\"/shared/audio/test.mp3\""
        self.assertEqual(converted, expected)

    


if __name__ == "__main__":
    unittest.main()