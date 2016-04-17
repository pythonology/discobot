import re
import os

from discord import game

from disco import bot, constants, config, redis_client


@bot.command(pass_context=True)
async def join(ctx):
    if ctx.message.author.voice_channel is None:
        return
    if bot.voice is not None:
        await bot.voice.disconnect()
    await bot.join_voice_channel(ctx.message.author.voice_channel)


@bot.command()
async def play(uri: str):
    if not bot.is_voice_connected():
        return

    after = lambda: bot.loop.create_task(bot.change_status(game=game.Game()))

    match = re.match(constants.RE_ATTACHMENT_URI, uri)
    if match is not None:
        if not config['attachments']['enabled']:
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
        if not config['youtube']['enabled']:
            await bot.say('Support for YouTube is currently disabled.')
            return

        await bot.play_youtube(uri, after=after)
        return

    match = re.match(constants.RE_SOUNDCLOUD_URL, uri)
    if match is not None:
        if not config['soundcloud']['enabled']:
            await bot.say('Support for Soundcloud is currently disabled.')
            return

        await bot.play_soundcloud(uri, after=after)
        return

    await bot.say('Invalid URI.')


@bot.command()
async def stop():
    if not bot.is_voice_connected():
        return
    if bot.player is not None:
        bot.player.stop()


@bot.command()
async def pause():
    if not bot.is_voice_connected():
        return
    if bot.player is not None:
        bot.player.pause()


@bot.command()
async def resume():
    if not bot.is_voice_connected():
        return
    if bot.player is not None:
        bot.player.resume()


@bot.command(pass_context=True)
async def aliases(ctx):
    aliases = {}
    for alias in redis_client.smembers('aliases'):
        alias = alias.decode('utf-8')
        key = 'aliases:' + alias
        if redis_client.hget(key, 'discriminator') != \
                ctx.message.author.discriminator.encode('utf-8'):
            continue
        aliases[alias] = redis_client.hget(key, 'uri').decode('utf-8')

    if not aliases:
        await bot.say('No aliases found.')
    else:
        quote = ''
        for key, value in aliases.items():
            quote += '%s: %s\n' % (key, value)
        await bot.say(quote.rstrip())


@bot.command(pass_context=True)
async def bind(ctx, alias: str, uri: str):
    if not alias or ' ' in alias or alias.startswith('<@'):
        await bot.say('Invalid alias.')
        return

    if alias.encode('utf-8') in redis_client.smembers('aliases'):
        await bot.say('That alias is already taken!')
        return

    redis_client.sadd('aliases', alias)
    redis_client.hmset(
        'aliases:' + alias,
        {'discriminator': ctx.message.author.discriminator, 'uri': uri})
    await bot.say('Done! The alias %s may now be used.' % alias)


@bot.command(pass_context=True)
async def unbind(ctx, alias: str):
    if alias.encode('utf-8') not in redis_client.smembers('aliases'):
        await bot.say('That alias does not exist!')
        return

    key = 'aliases:' + alias
    if redis_client.hget(key, 'discriminator') != \
            ctx.message.author.discriminator.encode('utf-8'):
        await bot.say('You did not create that alias.')
        return

    redis_client.srem('aliases', alias)
    redis_client.hdel(key, 'discriminator')
    redis_client.hdel(key, 'uri')
    await bot.say('Successfully deleted the alias %s.' % alias)
