#!/usr/bin/env python3
from disco import bot, config


@bot.event
async def on_ready():
    print('test')


if __name__ == '__main__':
    bot.run(config['token'])
