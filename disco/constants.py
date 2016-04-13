import re

SPOTIFY_SERVICE = 1
SOUNDCLOUD_SERVICE = 2

VALID_ATTACHMENT_TYPES = ('.ogg',)

# Regular expressions
RE_ATTACHMENT_URI = re.compile('^disco:\/\/(.*)\/(.*)$')
