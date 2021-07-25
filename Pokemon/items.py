# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from urllib import parse

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst, Identity
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class PokemonItemLoader(ItemLoader):
    """Itemloader for generating pokemon item from htmlResponse"""
    default_output_processor = TakeFirst()


def remove_html_tag(value):
    """Remove all html tag

    Args:
        value: A string converted from html text

    Returns:
        A string that all html tags removed
    """
    value = re.sub(r'(<style.*</style>)|(<script.*</script>)', '', value)
    return remove_tags(value)


def filter_duplicate_links(values):
    """Removes links that do not belong to the same domain, as well as home page

    Args:
        values: A list of url strings

    Returns:
        A list of links without external urls and home page url
    """
    links = set()
    for value in values:
        if re.match(r'^/wiki/[^:]+$', value) and not re.match('wiki/Main_Page', value):
            links.add(parse.urljoin('https://bulbapedia.bulbagarden.net/', value))
    return list(links)


class PokemonItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(remove_html_tag)
    )
    links = scrapy.Field(
        input_processor=Compose(filter_duplicate_links),
        output_processor=Identity()
    )
