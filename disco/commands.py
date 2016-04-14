import re
import os

from discord import game

from disco import bot, constants, redis_client


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

    # TODO: Use regular expressions when validating each URL.
    if 'spotify' in uri:
        bot.service = constants.SPOTIFY_SERVICE
        return

    match = re.match(constants.RE_YOUTUBE_URI, uri)
    if match is not None:
        player = await bot.voice.create_ytdl_player(uri, after=after)
        if bot.play(player):
            await bot.change_status(game=game.Game(name=bot.player.title))

        return

    match = re.match(constants.RE_SOUNDCLOUD_URI, uri)
    if match is not None:
        player = bot.create_soundcloud_player(uri, after=after)
        if bot.play(player):
            await bot.change_status(game=game.Game(name=bot.player.title))

        return

    match = re.match(constants.RE_ATTACHMENT_URI, uri)
    if match is not None:
        discriminator = match.group(1)
        filename = match.group(2)

        path = os.path.join('attachments', discriminator, filename)
        if not os.path.exists(path):
            await bot.say('That attachment does not exist!')
            return

        player = bot.voice.create_ffmpeg_player(path, after=after)
        if bot.play(player):
            await bot.change_status(game=game.Game(name=filename))

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
