import re

SPOTIFY_SERVICE = 1
SOUNDCLOUD_SERVICE = 2

VALID_ATTACHMENT_TYPES = ('.opus', '.weba', '.ogg', '.wav', '.mp3', '.flac',
                          '.midi')

# Regular expressions
RE_ATTACHMENT_URI = re.compile('^disco:\/\/(\d*)\/(.*)$')
RE_YOUTUBE_URI = re.compile(
    '^'
    '(?:https?:\/\/)'
    '(?:www\.)?'
    '(?:youtu(?:be\.com\/watch\?v=|\.be\/))'
    '([A-Za-z0-9_-]{11})'
    '(?:&[^=]+=[^&]+)*'
    '$'
)
RE_SOUNDCLOUD_URI = re.compile(
    '^'
    '(?:https?:\/\/)'
    '(?:www\.)?'
    '(?:soundcloud\.com\/)'
    '([A-Za-z0-9_-]+)'
    '(?:\/)'
    '([A-Za-z0-9_-]+)'
    '(?:\/)?'
    '(?:(?:\?|&)[^=]+=[^&]+)*'
    '$'
)
