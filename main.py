#!/usr/bin/env python3
import logging

from disco import bot, config

if __name__ == '__main__':
    log_config = config.get('log', {})
    level_name = log_config.pop('level', 'info').upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, **log_config)

    bot.run(config['bot']['token'])
