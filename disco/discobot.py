from discord.ext import commands


class DiscoBot(commands.Bot):
    def __init__(self):
        commands.Bot.__init__(self, commands.when_mentioned)

        self.service = None
