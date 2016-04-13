import re
import os

from disco import bot, constants


@bot.command(pass_context=True)
async def join(ctx):
    if ctx.message.author.voice_channel is None:
        return
    if bot.voice is not None:
        await bot.voice.disconnect()
    await bot.join_voice_channel(ctx.message.author.voice_channel)


@bot.command()
async def play(uri: str):
    # TODO: Use regular expressions when validating each URL.
    if 'spotify' in uri:
        bot.service = constants.SPOTIFY_SERVICE
        return

    match = re.match(constants.RE_ATTACHMENT_URI, uri)
    if match is not None:
        owner_name = match.group(1)
        filename = match.group(2)

        path = os.path.join('attachments', owner_name, filename)
        if not os.path.exists(path):
            await bot.say('That attachment does not exist!')
            return

        if bot.play(path):
            await bot.say('Now playing: ' + filename)

        return

    await bot.say('Invalid URI.')
