import logging
import aiohttp
import os

from discord.ext import commands
from discord import game

from disco import utils, soundcloud_client

log = logging.getLogger(__name__)


class DiscoBot(commands.Bot):
    def __init__(self, command_prefix, formatter=None, description=None,
                 pm_help=False, **options):
        commands.Bot.__init__(self, command_prefix, formatter=formatter,
                              description=description, pm_help=pm_help,
                              **options)

        self.player = None

    def create_soundcloud_player(self, url, **kwargs):
        log.info('playing URL ' + url)

        track = soundcloud_client.get('/resolve', url=url)
        stream_url = soundcloud_client.get(
            track.stream_url, allow_redirects=False)

        player = self.voice.create_ffmpeg_player(stream_url.location, **kwargs)

        player.stream_url = stream_url
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
