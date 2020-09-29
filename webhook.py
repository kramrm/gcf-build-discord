import requests
import json
import os

def post_webhook(message, timestamp, title='Status', color=0):
    url = os.environ.get('WEBHOOK')
    data = {}
    data['embeds'] = []
    embed = {}
    embed['title'] = f'Cloud Build {title}'
    embed['description'] = message
    embed['footer'] = {}
    embed['footer']['text'] = f'{title}'
    embed['timestamp'] = timestamp
    embed['color'] = color
    data['embeds'].append(embed)
    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return result