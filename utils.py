import json

from wit import Wit
from pprint import pprint
from gnewsclient import gnewsclient

TOKEN = 'KHCSJONZHILRWYLXAJMICQBJSQ5S2Z4J'
client = Wit(TOKEN)


def wit_response(message):
    response = client.message(message)
    pprint(response)
    categories = {'newstype': None, 'location': None}

    entites = list(response['entities'])
    for entity in entites:
        categories[entity] = response['entities'][entity][0]['value']

    return categories
def isGreeting(message):
    response = client.message(message)
    pprint(response)
    if response['entities'].get('greetings'):
        return True
    else:
        return False

print(isGreeting("Hey There"))

def get_news_elements(categories):
    news_client = gnewsclient()
    news_client.query = ''
    if categories['newstype'] != None:
        news_client.query += categories['newstype']

    if categories['location'] != None:
        news_client.query += categories['location']

    news_item = news_client.get_news()
    elements = []
    pprint(categories)
    for item in news_item:
        element = {
            'title': item['title'],
            'buttons': [
                {
                    'type': 'web_url',
                    'url': item['link'],
                    'title': 'Read More'
                }
            ],
            'image_url': item['img']
        }
        elements.append(element)

    return elements
