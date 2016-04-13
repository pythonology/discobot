import re
import os

from disco import bot, constants


@bot.command()
async def play(uri: str):
    # TODO: Use regular expressions when validating each URL.
    if 'spotify' in uri:
        bot.service = constants.SPOTIFY_SERVICE
    else:
        match = re.match(constants.RE_ATTACHMENT_URI, uri)
        if match is None:
            await bot.say('Invalid URI.')
            return

        author_name = match.group(1)
        filename = match.group(2)

        path = os.path.join('attachments', author_name, filename)
        if not os.path.exists(path):
            await bot.say('This attachment does not exist!')
            return

        await bot.say("I can't do that yet.")
