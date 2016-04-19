#!/usr/bin/env python3
"""A fully-featured music bot for Discord."""

import argparse
import yaml
import logging

from discord import opus

from discobot import bot


def main():
    """
    The main entry point.

    Invoke using either `disco` or `python -m disco`.
    """
    parser = argparse.ArgumentParser(
        prog='disco', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'config', nargs='?', type=argparse.FileType('r'),
        default='config.yaml', help='configuration file to use')
    args = parser.parse_args()

    config = yaml.load(args.config.read())
    args.config.close()

    kwargs = config.get('log', {}).copy()
    level = getattr(logging, kwargs.pop('level', 'info').upper(), logging.INFO)
    logging.basicConfig(level=level, **kwargs)

    if not opus.is_loaded():
        opus.load_opus(config['opus_library_path'])

    bot.configure(config)
    bot.run(config['bot']['token'])


if __name__ == '__main__':
    main()
