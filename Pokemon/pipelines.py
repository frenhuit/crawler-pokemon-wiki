# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from Pokemon.models.es_types import PokemonType
from elasticsearch_dsl.connections import connections
from twisted.internet import reactor, defer

es = connections.create_connection(hosts=['localhost'])


def gen_suggests(weight_tuples):
    """Returns search suggestions with search weight defined.

    Args:
        weight_tuples: A list of tuples including text and weight.

    Returns:
        A dict including word list and weight
        example:

        {'input': ['Pokemon', 'Poke'], 'weight': 10,
         'input': ['Pocket Monster'], 'weight': 5}
    """
    used_words = set()
    suggests = []
    for weight_tuple in weight_tuples:
        (text, weight) = weight_tuple
        new_words = set()
        if text:
            tokens = es.indices.analyze(
                                        body={'text': text, 'analyzer': 'english'})['tokens']
            words = set()
            for token in tokens:
                words.add(token['token'])
            new_words = words - used_words
        if new_words:
            suggests.append({'input': list(new_words), 'weight': weight})
    return suggests


class MongoDBTwistedPipeline(object):
    """A pipeline for asynchronous insertion into MongoDB"""
    def __init__(self, mongo_uri, mongo_db, mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB'),
            mongo_col=crawler.settings.get('MONGODB_COLLECTION'),
        )

    def open_spider(self, spider):
        """Runs after crawler starts."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.mongodb = self.client[self.mongo_db]

    def close_spider(self, spider):
        """Runs before crawler ends."""
        self.client.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        out = defer.Deferred()
        reactor.callInThread(self._insert, item, out, spider)
        yield out
        defer.returnValue(item)

    def _insert(self, item, out, spider):
        """Inserts item

        Args:
            item: Item object
            out: Deferred object
            spider: Crawler

        """
        self.mongodb[self.mongo_col].update({'url': item['url']}, dict(item), True)
        reactor.callFromThread(out.callback, item)


class ElasticSearchPipeline(object):
    """A pipeline for insertion into ElasticSearch"""
    def process_item(self, item, spider):
        pokemon = PokemonType(_id=item['url'])
        pokemon.url = item['url']
        pokemon.title = item['title']
        pokemon.content = item['content']
        pokemon.links = item['links']
        pokemon.suggest = gen_suggests([(pokemon.title, 100), (pokemon.content, 1)])
        pokemon.save()
        return item
