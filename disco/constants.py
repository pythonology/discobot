import re

SPOTIFY_SERVICE = 1
SOUNDCLOUD_SERVICE = 2

VALID_ATTACHMENT_TYPES = ('.opus', '.weba', '.ogg', '.wav', '.mp3', '.flac',
                          '.midi')

# Regular expressions
RE_ATTACHMENT_URI = re.compile('^disco:\/\/(\d*)\/(.*)$')
