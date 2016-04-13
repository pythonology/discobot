import json
import logging

from discord import opus
from discord.ext import commands

from disco import discobot

with open('config.json') as f:
    config = json.load(f)

format = '%(asctime)s ::%(levelname)s:: %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = getattr(logging, config.get('log-level', 'info').upper())
logging.basicConfig(format=format, datefmt=datefmt, level=level)

if not opus.is_loaded():
    opus.load_opus(config['opus-library-path'])

bot = discobot.DiscoBot(commands.when_mentioned)

import disco.events
import disco.commands
