import os

from disco import bot, constants

from discord import channel


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, channel.PrivateChannel):
        for attachment in message.attachments:
            filename = attachment['filename']

            ext = os.path.splitext(filename)[1]
            if ext not in constants.VALID_ATTACHMENT_TYPES:
                await bot.send_message(
                    message.channel,
                    'File type %s is not supported! It must be one of the '
                    'following: %s' %
                    (ext, ', '.join(constants.VALID_ATTACHMENT_TYPES)))
                continue

            await bot.send_message(
                message.channel, 'Downloading %s...' % filename)
            uri = await bot.download_attachment(message.author, attachment)
            await bot.send_message(
                message.channel,
                'Done! To play this attachment, use: %s play %s' %
                (bot.user.mention, uri))
