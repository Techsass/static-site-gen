import unittest

from nodehelpers import *

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://dood.site/example")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://dood.site/example"})

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://dood.site/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src":"https://dood.site/image.png", "alt":"This is a image node"})

class TestSplitNodeByDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(nodes, expected)

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(nodes, expected)

    def test_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(nodes, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "This is text without an image"
        )
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_multi(self):
        matches = extract_markdown_images(
            "This is text with multiple images ![funny](https://pbs.twimg.com/media/Fj4PkQeWQAEVUFL.jpg) and another one here ![FAAAAAA](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7ZtQ6SXheMMzMsYOokeT4nzWLAlgbXEG-3g&s)"
        )
        self.assertListEqual([("funny", "https://pbs.twimg.com/media/Fj4PkQeWQAEVUFL.jpg"), ("FAAAAAA", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7ZtQ6SXheMMzMsYOokeT4nzWLAlgbXEG-3g&s")], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [link to meme](https://www.youtube.com/watch?v=9t9pDnG0SeM)"
        )
        self.assertListEqual([("link to meme", "https://www.youtube.com/watch?v=9t9pDnG0SeM")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This is text with no links"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multi(self):
        matches = extract_markdown_links(
            "This is text with a multiple links [meme](https://www.youtube.com/watch?v=9t9pDnG0SeM) and [dood](https://www.yourdictionary.com/dood)"
        )
        self.assertListEqual([("meme", "https://www.youtube.com/watch?v=9t9pDnG0SeM"), ("dood", "https://www.yourdictionary.com/dood")], matches)

class TestLinkImageSplits(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_start(self):
        node = TextNode(
            "![image to start](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image to start", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_start(self):
        node = TextNode(
            "[link to start](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link to start", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_start_text_after(self):
        node = TextNode(
            "![image to start](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image to start", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(
                " and text after", TextType.TEXT
                )
            ],
            new_nodes,
        )

    def test_split_links_start_text_after(self):
        node = TextNode(
            "[link to start](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link to start", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and text after", TextType.TEXT),
            ],
            new_nodes,
        )

class TestFullSplit(unittest.TestCase):
    def test_full_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        split = text_to_textnodes(text)
        # print("split", split)
        expected = [
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
            ]
        self.assertListEqual(expected, split)
