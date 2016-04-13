from disco import bot, constants


@bot.command()
async def play(url: str):
    if 'spotify' in url:
        bot.service = constants.SPOTIFY_SERVICE
    else:
        await bot.say(
            "I don't know what music streaming service you're trying to "
            "access.")
