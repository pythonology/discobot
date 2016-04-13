import re
import os

from discord import channel

from disco import bot, constants, utils


@bot.listen()
async def on_ready():
    await bot.change_status()


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, channel.PrivateChannel):
        if not message.attachments:
            match = re.match(constants.RE_ATTACHMENT_URI, message.content)
            if match is not None:
                owner_name = match.group(1)
                filename = match.group(2)

                path = os.path.join('attachments', owner_name, filename)
                if message.author.name == owner_name and os.path.exists(path):
                    await bot.send_message(
                        message.channel, 'Deleting %s...' % filename)
                    os.remove(path)
                    dirname = os.path.dirname(path)
                    if not os.listdir(dirname):
                        os.rmdir(dirname)
                    return

            uris = []
            path = os.path.join('attachments', message.author.name)
            if os.path.exists(path):
                for filename in os.listdir(path):
                    uri = utils.make_attachment_uri(
                        message.author.name, filename)
                    uris.append(uri)
            quote = 'That attachment does not exist!\n\nIf you wish to ' \
                    'delete one of your submitted attachments, you must ' \
                    'provide its URI. '
            if uris:
                quote += 'Here is a list of all of your submitted ' \
                         'attachments:\n' + '\n'.join(uris)
            else:
                quote += 'You currently have no submitted attachments.'
            await bot.send_message(message.channel, quote)
            return

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
