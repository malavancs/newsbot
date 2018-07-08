import os
import sys
import json
from datetime import datetime
from pprint import pprint
from utils import wit_response, isGreeting
from utils import get_news_elements
from credentials import VERIFY_TOKEN,PAGE_ACCESS_TOKEN
import requests
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)
exceptionGOT = 'greetings'
bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    data = request.get_json()
    log(data)
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/privacy',methods=['GET'])
def privacy_policy():

    value = "<h1>News Bot <h1><br><P>We do not collect or use any user's data from our chatbot<P>"
    return value,200


@app.route('/', methods=['POST'])
def webhook():
    elements = []
    data = request.get_json()

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                message_text = "No text"

                if messaging_event.get('message'):

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event["message"]['text']
                        if isGreeting(message_text):
                            bot.send_text_message(sender_id, "Hi there, I am a Newsbot , I know news :)")
                            return 'ok', 200
                    else:
                        message_text = "No text"
                    response = wit_response(message_text)

                    if response['newstype']!=None:
                        if response['location']!=None:
                            elements = get_news_elements(response)
                            pprint(bot.send_generic_message(sender_id, elements))
                        else:
                            elements = get_news_elements(response)
                            pprint(bot.send_generic_message(sender_id, elements))

                    else:
                        if response['location']!=None:
                            elements = get_news_elements(response)
                            pprint(bot.send_generic_message(sender_id, elements))
                        else:
                            bot.send_text_message(sender_id, "Try something else")

    return 'ok', 200


def log(msg):
    pprint(msg)


if __name__ == '__main__':
    app.run(debug=True)
