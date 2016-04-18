import re
import os

from discord import channel

from disco import bot, config, constants, utils, redis_client


@bot.listen()
async def on_message(message):
    # We don't want to parse the bot's own messages.
    if message.author == bot.user:
        return

    # Private messages are used only for managing attachments.
    if isinstance(message.channel, channel.PrivateChannel):
        if not config.get('attachments', {}).get('enabled', False):
            await bot.send_message(
                message.channel,
                'Support for attachments is currently disabled.')
            return

        # If the user isn't sending any attachments, assume that they
        # are trying to delete one of their previously submitted ones.
        if not message.attachments:
            match = re.match(constants.RE_ATTACHMENT_URI, message.content)
            if match is not None:
                # Only delete the specified attachment if they own it.
                if match.group(1) == message.author.discriminator:
                    await bot.send_message(
                        message.channel, 'Deleting %s...' % message.content)
                    bot.delete_attachment(message.content)
                    return

            # The user hasn't specified an existing attachment to
            # delete. Let's help them out and list all of their
            # previously submitted attachments.
            quote = 'That attachment does not exist!\n\nIf you wish to ' \
                    'delete one of your submitted attachments, you must ' \
                    'provide its URI. '
            uris = []
            path = os.path.join('attachments', message.author.discriminator)
            if os.path.exists(path):
                for filename in os.listdir(path):
                    uris.append(
                        utils.make_attachment_uri(
                            message.author.discriminator, filename))
            if uris:
                quote += 'Here is a list of all of your previously ' \
                         'submitted attachments:\n' + '\n'.join(uris)
            else:
                quote += 'You currently have no submitted attachments.'
            await bot.send_message(message.channel, quote)
            return

        # The user is sending attachments. Let's download all of the
        # ones with valid extensions, and generate URIs for them.
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
    else:
        # The user may be trying to use an alias.
        if message.content.encode('utf-8') in redis_client.smembers('aliases'):
            uri = redis_client.hget('aliases:' + message.content, 'uri')

            # Overwrite message.content so that we can invoke the play
            # command without doing too much extra work.
            command_prefix = bot.command_prefix
            if callable(command_prefix):
                command_prefix = command_prefix(bot, message)
            if isinstance(command_prefix, (tuple, list)):
                command_prefix = command_prefix[0]
            message.content = command_prefix + 'play ' + uri.decode('utf-8')
            await bot.process_commands(message)
