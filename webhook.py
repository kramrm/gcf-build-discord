import requests
import json
import os

def post_webhook(message, timestamp, title='Status', color=0):
    """Post webhook to Discord
    Set an environment variable for 'WEBHOOK' to point to the URI for your channel
    
    Attributes
        message (str): The message to put in the embed
        timestamp (str): ISO 8601 timestamp of the event
        title (str): Stats of the build process for the embed title.  Defaults to 'Status'
        color (int): Color to use for embed highlight. Defaults to black
    """
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
