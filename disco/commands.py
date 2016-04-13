import re
import os

from disco import bot, constants


@bot.command()
async def play(uri: str):
    # TODO: Use regular expressions when validating each URL.
    if 'spotify' in uri:
        bot.service = constants.SPOTIFY_SERVICE
        return

    match = re.match(constants.RE_ATTACHMENT_URI, uri)
    if match is not None:
        author_name = match.group(1)
        filename = match.group(2)

        path = os.path.join('attachments', author_name, filename)
        if not os.path.exists(path):
            await bot.say('That attachment does not exist!')
            return

        await bot.say("I can't do that yet.")

    await bot.say('Invalid URI.')
