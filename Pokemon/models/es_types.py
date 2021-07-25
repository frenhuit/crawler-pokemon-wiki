from elasticsearch_dsl import Document, Keyword, Text, Completion

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])


class PokemonType(Document):
    """Pokemon type used in Elasticsearch"""
    url = Keyword()
    title = Keyword()
    content = Text()
    links = Keyword()
    suggest = Completion()

    class Index:
        name = 'pokemon3'
        settings = {"number_of_shards": 3, "number_of_replicas": 1}


if __name__ == '__main__':
    connections.create_connection()
    PokemonType.init()
