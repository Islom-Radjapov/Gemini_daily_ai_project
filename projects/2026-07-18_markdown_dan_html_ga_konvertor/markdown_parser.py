import re

class MarkdownParser:
    """
    A simple Markdown to HTML parser using only standard Python libraries.
    Supports a subset of Markdown syntax for block and inline elements.
    """

    def _escape_html(self, text: str) -> str:
        """Escapes special HTML characters in a string to prevent XSS and ensure valid HTML."""
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&#39;")
        return text

    def _parse_inline_elements(self, text: str) -> str:
        """
        Parses and converts inline Markdown elements to HTML.
        This function assumes the input `text` has already had raw HTML characters escaped.
        Supported inline elements: bold, italic, inline code, links.
        Order of replacement matters to avoid misinterpreting escaped chars or nested markdown.
        """
        # Inline code: `code`
        # Matches content between backticks. Content is assumed to be escaped.
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

        # Links: [text](url)
        # Matches link text and URL, which are then used in an <a> tag.
        # Captured groups (\1 for text, \2 for URL) are already HTML-escaped.
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

        # Bold: **text** or __text__
        # Matches content between double asterisks or double underscores.
        text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)

        # Italic: *text* or _text_
        # Matches content between single asterisks or single underscores.
        text = re.sub(r"\*([^\*]+)\*", r"<em>\1</em>", text)
        text = re.sub(r"_([^_]+)_", r"<em>\1</em>", text)
        
        return text

    def parse(self, markdown_text: str) -> str:
        """
        Parses a given Markdown text string and returns its HTML representation.
        It processes the input line by line to identify and convert blocks.
        """
        html_parts = []
        lines = markdown_text.splitlines()
        num_lines = len(lines)
        i = 0

        while i < num_lines:
            line = lines[i].strip()

            # Skip initial consecutive blank lines
            if not line and not html_parts:
                i += 1
                continue

            # Headings: # H1, ## H2, ..., ###### H6
            heading_match = re.match(r"^(#+)\s*(.*)", line)
            if heading_match:
                level = len(heading_match.group(1))
                # Escape HTML in content, then parse inline Markdown
                content = self._parse_inline_elements(self._escape_html(heading_match.group(2).strip()))
                html_parts.append(f"<h{level}>{content}</h{level}>")
                i += 1
                continue

            # Horizontal Rule: --- or *** (on a line by itself)
            # Allows for optional spaces between asterisks
            if re.match(r"^(-{3,}|(\* *){3,})$", line):
                html_parts.append("<hr>")
                i += 1
                continue

            # Fenced Code Blocks: