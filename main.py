#!/usr/bin/env python3
import logging

from disco import bot, config

if __name__ == '__main__':
    kwargs = config.get('log', {})
    level = getattr(logging, kwargs.pop('level', 'info').upper(), logging.INFO)
    logging.basicConfig(level=level, **kwargs)

    bot.run(config['bot']['token'])
