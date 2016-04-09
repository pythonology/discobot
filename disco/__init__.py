import json

from disco import discobot


with open('config.json', 'r') as f:
    config = json.load(f)

bot = discobot.DiscoBot()
