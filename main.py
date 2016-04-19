#!/usr/bin/env python3
import yaml
import logging

from discord import opus

from disco import bot

if __name__ == '__main__':
    with open('config.yaml') as f:
        config = yaml.load(f)

    kwargs = config.get('log', {}).copy()
    level = getattr(logging, kwargs.pop('level', 'info').upper(), logging.INFO)
    logging.basicConfig(level=level, **kwargs)

    if not opus.is_loaded():
        opus.load_opus(config['opus_library_path'])

    bot.configure(config)
    bot.run(config['bot']['token'])
