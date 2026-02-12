import unittest
from blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
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
        
    def test_markdown_to_blocks_details(self):
        md = """
### 3. Collapsible Details Block
<details>
<summary>Click to expand logs</summary>

```
2025-11-22 15:05:12 ERROR  Token validation failed
2025-11-22 15:05:13 INFO   Retrying request...
2025-11-22 15:05:14 OK     Token refreshed successfully
```

</details>
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "### 3. Collapsible Details Block\n<details>\n<summary>Click to expand logs</summary>",
                "```\n2025-11-22 15:05:12 ERROR  Token validation failed\n2025-11-22 15:05:13 INFO   Retrying request...\n2025-11-22 15:05:14 OK     Token refreshed successfully\n```",
                "</details>",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_blocktype_multi(self):
        md = """
        ##### This is a header

        This is **bolded** paragraph

        > This is another paragraph with _italic_ text and `code` here
        > This is the same paragraph on a new line

        - This is a list
        - with items

        ```
        HUGE CODE BLOCK
        ```

        """
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertEqual(
            blocktypes,
            [   
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.CODE,
            ],
        )
    
    def test_block_to_blocktype_ordered_list(self):
        md = """
        1. TEST
        2. TEST
        3. TEST

        3. TEST
        2. TEST
        1. TEST
        """
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertEqual(
            blocktypes,
            [
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
            ],
        )

class TestMDToHTMLNodes(unittest.TestCase):
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

class TestTitleExtraction(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        # header header check check

        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
        
        title = extract_title(md)
        self.assertEqual(
            title,
            "header header check check",
        )

    def test_codeblock(self):
        md = """
        ## not this one
        # eyerrrr

        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        title = extract_title(md)
        self.assertEqual(
            title,
            "eyerrrr",
        )