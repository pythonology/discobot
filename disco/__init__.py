import json
import logging

from discord.ext import commands

from disco import discobot

with open('config.json') as f:
    config = json.load(f)

format = '%(asctime)s ::%(levelname)s:: %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = getattr(logging, config.get('log-level', 'info').upper())
logging.basicConfig(format=format, datefmt=datefmt, level=level)

bot = discobot.DiscoBot(commands.when_mentioned)

import disco.events
import disco.commands
