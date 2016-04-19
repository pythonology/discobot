import redis
import soundcloud
import logging
import aiohttp
import os
import re

from discord.ext import commands
from discord import game

from discobot import utils, constants

log = logging.getLogger(__name__)


class DiscoBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = {}
        self.redis = None
        self.soundcloud = None
        self.player = None

    def configure(self, config):
        self.config = config

        self.command_prefix = config['bot']['command_prefix']
        if len(self.command_prefix) > 1:
            self.command_prefix = eval(self.command_prefix)

        self.redis = redis.StrictRedis(**config['redis'])

        if config['soundcloud']['enabled']:
            self.soundcloud = soundcloud.Client(**config['soundcloud'])

    def create_soundcloud_player(self, url, **kwargs):
        log.info('playing URL ' + url)

        track = self.soundcloud.get('/resolve', url=url)
        stream_url = self.soundcloud.get(
            track.stream_url, allow_redirects=False)

        player = self.voice.create_ffmpeg_player(stream_url.location, **kwargs)
        player.stream_url = stream_url.location
        player.url = url
        player.uploader = track.label_name or track.user['username']
        player.title = track.title
        return player

    def play(self, player):
        if not self.is_voice_connected():
            return False
        if self.player is not None and self.player.is_playing():
            self.player.after = None
            self.player.stop()
        self.player = player
        self.player.start()
        return True

    async def play_attachment(self, path, after=None):
        player = self.voice.create_ffmpeg_player(path, after=after)
        if self.play(player):
            basename = os.path.basename(path)
            await self.change_status(game=game.Game(name=basename))

    async def play_youtube(self, url, after=None):
        player = await self.voice.create_ytdl_player(url, after=after)
        if self.play(player):
            await self.change_status(game=game.Game(name=self.player.title))

    async def play_soundcloud(self, url, after=None):
        player = self.create_soundcloud_player(url, after=after)
        if self.play(player):
            await self.change_status(game=game.Game(name=self.player.title))

    async def download_attachment(self, author, attachment):
        path = os.path.join('attachments', author.discriminator)
        if not os.path.exists(path):
            os.makedirs(path)

        url = attachment['url']
        filename = attachment['filename']

        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(os.path.join(path, filename), 'wb') as f:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)

        return utils.make_attachment_uri(author.discriminator, filename)

    def delete_attachment(self, uri):
        match = re.match(constants.RE_ATTACHMENT_URI, uri)
        if match is None:
            return False

        discriminator = match.group(1)
        filename = match.group(2)

        path = os.path.join('attachments', discriminator, filename)
        if not os.path.exists(path):
            return False

        os.remove(path)
        dirname = os.path.dirname(path)
        if not os.listdir(dirname):
            os.rmdir(dirname)

        return True
