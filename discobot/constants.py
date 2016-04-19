import re

VALID_ATTACHMENT_TYPES = ('.opus', '.weba', '.ogg', '.wav', '.mp3', '.flac',
                          '.midi')

# Regular expressions
RE_ATTACHMENT_URI = re.compile(
    '^'
    '(?:disco:\/\/)'
    '(\d+)'
    '(?:\/)'
    '([\w\-\.]+)'
    '$'
)
RE_YOUTUBE_URL = re.compile(
    '^'
    '(?:https?:\/\/)'
    '(?:www\.)?'
    '(?:youtu(?:be\.com\/watch\?v=|\.be\/))'
    '([\w-]{11})'
    '(?:&(?:[^=]+=[^&])+)?'
    '$'
)
RE_SOUNDCLOUD_URL = re.compile(
    '^'
    '(?:https?:\/\/)'
    '(?:www\.)?'
    '(?:soundcloud\.com\/)'
    '([\w-]+)'
    '(?:\/)'
    '([\w-]+)'
    '(?:\/)?'
    '(?:\?(?:[^=]+=[^&])+)?'
    '$'
)
RE_ALIAS = re.compile(
    '^'
    '(?!<@)'
    '([^\w\s])'
    '([^\s]+)'
    '$'
)
