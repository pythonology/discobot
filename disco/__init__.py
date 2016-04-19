import yaml

import redis
import soundcloud
from discord import opus
from discord.ext import commands

with open('config.yml') as f:
    config = yaml.load(f)

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
