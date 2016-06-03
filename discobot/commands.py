import re
import os

from discord import game

from discobot import bot, __version__, constants


@bot.command()
async def version():
    """Responds with the version of Discobot that is being run."""
    await bot.say(__version__)


@bot.command(pass_context=True)
async def join(ctx):
    """Makes Discobot join your current voice channel."""
    channel = ctx.message.author.voice_channel
    if channel is None:
        return
    if bot.is_voice_connected(channel.server):
        await bot.voice.disconnect()
    await bot.join_voice_channel(channel)


@bot.command(pass_context=True)
async def play(ctx, uri: str):
    """Plays the track of your choice."""
    if not bot.is_voice_connected(ctx.message.server):
        return

    after = lambda: bot.loop.create_task(bot.change_status(game=game.Game()))

    match = re.match(constants.RE_ATTACHMENT_URI, uri)
    if match is not None:
        if not bot.config['attachments']['enabled']:
            await bot.say('Support for attachments is currently disabled.')
            return

        discriminator = match.group(1)
        filename = match.group(2)
        path = os.path.join('attachments', discriminator, filename)
        if not os.path.exists(path):
            await bot.say('That attachment does not exist!')
            return

        await bot.play_attachment(path, after=after)
        return

    match = re.match(constants.RE_YOUTUBE_URL, uri)
    if match is not None:
        if not bot.config['youtube']['enabled']:
            await bot.say('Support for YouTube is currently disabled.')
            return

        await bot.play_youtube(uri, after=after)
        return

    match = re.match(constants.RE_SOUNDCLOUD_URL, uri)
    if match is not None:
        if not bot.config['soundcloud']['enabled']:
            await bot.say('Support for SoundCloud is currently disabled.')
            return

        await bot.play_soundcloud(uri, after=after)
        return

    await bot.say('Invalid URI.')


@bot.command(pass_context=True)
async def stop(ctx):
    """Stops the currently playing track."""
    if not bot.is_voice_connected(ctx.message.server):
        return
    if bot.player is not None:
        bot.player.stop()


@bot.command(pass_context=True)
async def pause(ctx):
    """Pauses the currently playing track."""
    if not bot.is_voice_connected(ctx.message.server):
        return
    if bot.player is not None:
        bot.player.pause()


@bot.command(pass_context=True)
async def resume(ctx):
    """Resumes the currently playing track."""
    if not bot.is_voice_connected(ctx.message.server):
        return
    if bot.player is not None:
        bot.player.resume()


@bot.group(pass_context=True)
async def aliases(ctx):
    """Lists registered aliases."""
    aliases = {}
    for alias in bot.redis.smembers('aliases'):
        alias = alias.decode('utf-8')
        key = 'aliases:' + alias
        discriminator = bot.redis.hget(key, 'discriminator').decode('utf-8')
        if ctx.subcommand_passed is None or \
                ctx.subcommand_passed == discriminator:
            aliases[alias] = bot.redis.hget(key, 'uri').decode('utf-8')

    if not aliases:
        await bot.say('No aliases found.')
    else:
        # TODO: Do these need to be sorted?
        quote = ''
        for key, value in aliases.items():
            quote += '%s: %s\n' % (key, value)
        await bot.say(quote.rstrip())


@bot.command(pass_context=True)
async def bind(ctx, alias: str, uri: str):
    """Binds an alias to the track of your choice."""
    if re.match(constants.RE_ALIAS, alias) is None:
        await bot.say('Invalid alias.')
        return

    if alias.encode('utf-8') in bot.redis.smembers('aliases'):
        await bot.say('That alias is already taken!')
        return

    bot.redis.sadd('aliases', alias)
    bot.redis.hmset(
        'aliases:' + alias,
        {'discriminator': ctx.message.author.discriminator, 'uri': uri})
    await bot.say('Done! The alias %s may now be used.' % alias)


@bot.command(pass_context=True)
async def unbind(ctx, alias: str):
    """Unbinds an alias."""
    if alias.encode('utf-8') not in bot.redis.smembers('aliases'):
        await bot.say('That alias does not exist!')
        return

    key = 'aliases:' + alias
    if bot.redis.hget(key, 'discriminator') != \
            ctx.message.author.discriminator.encode('utf-8'):
        await bot.say('You did not create that alias.')
        return

    bot.redis.srem('aliases', alias)
    bot.redis.hdel(key, 'discriminator')
    bot.redis.hdel(key, 'uri')
    await bot.say('Successfully deleted the alias %s.' % alias)
