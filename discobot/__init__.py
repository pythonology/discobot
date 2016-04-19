"""A fully-featured music bot for Discord."""

__version__ = '0.4.0'
__author__ = 'Chan, Pythonology'
__maintainer__ = 'Pythonology'
__license__ = 'MIT'

from discord.ext import commands

from discobot import bot

bot = bot.DiscoBot(commands.when_mentioned)

import discobot.events
import discobot.commands