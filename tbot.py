#!/usr/bin/env python3
from flask import Flask 
from flask import request
from flask import jsonify
import requests
import json
import re

from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

TOKEN = "726063502:AAExe44U7XO_riZ1jaCso4dim3uV1nC6nBc"
URL = f'https://api.telegram.org/bot{TOKEN}'

def write_json(data, filename='answer.json'):
	with open(filename, 'w') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='bla-bla-bla'):
	url = URL + '/sendMessage'
	answer = {'chat_id': chat_id, 'text': text}
	r = requests.post(url, json=answer)
	return r.json()

def parse_text(text):
	pattern = r'/\w+'
	crypto = re.search(pattern, text).group()
	return crypto

def get_price(crypto):
	url = f'https://api.coinmarketcap.com/v2/ticker/1/?convert={crypto}'
	r = requests.get(url).json()
	price = r[-1]['quotes']['USD']['price']
	return price

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		r = request.get_json()
		chat_id = r['message']['chat']['id']
		message = r['message']['text']
		print(chat_id, message)
		if 'bitcoin' in message:
			send_message(chat_id, text="Very big many")

		return jsonify(r)
	return '<h1>Bot welcomes you</h1>'

def main():
	app.run()


if __name__ == '__main__':
	main()


