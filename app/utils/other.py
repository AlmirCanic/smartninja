from HTMLParser import HTMLParser
import os
import sys


def convert_markdown_to_html(text):
    """"Converts markdown to html using markdown2 library"""
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../libs'))
    import markdown2
    markdowner = markdown2.Markdown()
    return markdowner.convert(text)


# HTML parser and tags stripper
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()