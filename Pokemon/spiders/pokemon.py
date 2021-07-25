# -*- coding: utf-8 -*-
from Pokemon.items import PokemonItemLoader, PokemonItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PokemonSpider(CrawlSpider):
    """Crawler for fetching response from Pokemon wiki"""
    name = 'pokemon'
    allowed_domains = ['bulbapedia.bulbagarden.net']
    start_urls = ['https://bulbapedia.bulbagarden.net/wiki/Mewtwo_(Pok%C3%A9mon)']

    rules = (
        Rule(LinkExtractor(allow=r'//bulbapedia.bulbagarden.net/wiki/.*',
                           deny=(r'//bulbapedia.bulbagarden.net/wiki/.+:.+', r'wiki/Main_Page',
                                 r'm.bulbapedia.bulbagarden.net/wiki/.*')),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """Analyzes response

        Args:
            response: A htmlResponse

        Returns:
            PokemonItem
        """
        item_loader = PokemonItemLoader(item=PokemonItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('title', '//h1[@id="firstHeading"]/text()')
        item_loader.add_xpath('content', '//div[@id="mw-content-text"]')
        item_loader.add_xpath('links', '//div[@id="bodyContent"]//a/@href')

        item = item_loader.load_item()
        return item
