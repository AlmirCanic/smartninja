from HTMLParser import HTMLParser
import logging
import os
import sys
from google.appengine.api import users
from app.models.course import Price
from app.models.partner import Partner


def convert_markdown_to_html(text):
    """"Converts markdown to html using markdown2 library"""
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../libs'))
    import markdown2
    markdowner = markdown2.Markdown()
    return markdowner.convert(text)


def convert_prices_data(data):
    """Converts prices data from course_add or course_edit to list of Price objects"""
    data = data[:-2]
    prices_data_list = data.split("{}")

    price_objects_list = []

    for prices_data in prices_data_list:
        single_data_list = prices_data.split("|")
        price = Price(price_dot=float(single_data_list[0]), price_comma=single_data_list[1], summary=single_data_list[2])
        price_objects_list.append(price)

    return price_objects_list


def convert_partners_data(data):
    if data == "":
        return []
    else:
        partner = Partner.get_by_id(int(data))
        return [partner]


def convert_tags_to_list(tags):
    tags = tags.split(",")

    new_tags = []

    for tag in tags:
        if tag.startswith(" "):
            tag = tag[1:]

        if tag.endswith(" "):
            tag = tag[:-1]

        new_tags.append(tag)

    return new_tags


def convert_tags_to_string(tags):
    tags_string = ""

    for tag in tags:
        tags_string += tag + ","

    return tags_string[:-1]


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


def logga(message):
    user = users.get_current_user()
    logging.info("Action by user %s: %s" % (user.email().lower(), message))