from discord.ext import commands

from disco import discobot

bot = discobot.DiscoBot(commands.when_mentioned)

import disco.events
import disco.commands
