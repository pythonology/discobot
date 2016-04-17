import yaml
import logging

import redis
import soundcloud
from discord import opus
from discord.ext import commands

with open('config.yml') as f:
    config = yaml.load(f)

log_config = config.get('log', {})
format = log_config.get('format', '%(asctime)s ::%(levelname)s:: %(message)s')
datefmt = log_config.get('datefmt', '%Y-%m-%d %H:%M:%S')
level = getattr(logging, log_config.get('level', 'info').upper())
logging.basicConfig(format=format, datefmt=datefmt, level=level)

redis_client = redis.StrictRedis(
    host=config['redis']['host'], port=config['redis']['port'],
    db=config['redis']['db'])

soundcloud_client = soundcloud.Client(
    client_id=config['soundcloud']['client_id'])

if not opus.is_loaded():
    opus.load_opus(config['opus_library_path'])

from disco import discobot

bot = discobot.DiscoBot(commands.when_mentioned)

import disco.events
import disco.commands
