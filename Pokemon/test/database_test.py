from elasticsearch import Elasticsearch
from pymongo import MongoClient

test_titles = [
    'Bulbasaur (Pokémon)',
    'Ivysaur (Pokémon)',
    'Venusaur (Pokémon)',
    'Charmander (Pokémon)',
    'Charmeleon (Pokémon)',
    'Charizard (Pokémon)',
    'Squirtle (Pokémon)',
    'Wartortle (Pokémon)',
    'Blastoise (Pokémon)',
    'Caterpie (Pokémon)',
]


def test_mongodb():
    print('Starts testing mongodb...')
    # Mongodb connection
    client = MongoClient('mongodb://10.0.0.22:27017/')
    db = client.search_engine
    collection = db.pokemon3

    for title in test_titles:
        query = {'title': title}
        result = collection.find_one(query)
        assert result is not None, 'Result should exist.'
    print('Mongodb passed.')


def test_elastic_search():
    print('Starts testing Elasticsearch...')
    client = Elasticsearch(hosts=['10.0.0.22:9200'])
    index = 'pokemon3'
    for title in test_titles:
        response = client.search(
            index=index,
            body={
                'query': {
                    'match': {
                        'title': title
                    }
                }
            }
        )
        assert response['hits']['total']['value'] > 0, "Result should exist."
    print('Elasticsearch passed.')


if __name__ == '__main__':
    test_mongodb()
    test_elastic_search()
    print('All passed.')
