import discord
from discord.ext import commands
import os
from time import time
import logging
from utils.logger import setup_logging
from config import TEST_GUILD_ID, STATUS, LOGGING, COLOR, BAD
from utils.timeconvert import datetime_to_unix
from datetime import timedelta


class JBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None, debug_guilds=[TEST_GUILD_ID])
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.start_time = time()
        for filename in os.listdir("functions"):
            if filename.endswith(".py"):
                self.load_extension(f"functions.{filename[:-3]}")
        self.logger.info(f"{len(self.extensions)} extensions are completely loaded")
        self.load_extension('jishaku')

    def run(self):
        super().run(os.environ['token'])

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name}")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(STATUS),
        )
        await self.wait_until_ready()

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        channel = await self.fetch_channel(LOGGING)
        embed = discord.Embed(title="메세지 수정됨", color=COLOR)
        embed.add_field(name="수정 전", value=f"```{before.content}```")
        embed.add_field(name="수정 후", value=f"```{after.content}```")
        embed.add_field(name="보낸 유저", value=after.author.mention)
        embed.add_field(name="채널", value=after.channel.mention)
        embed.add_field(name="메세지 링크", value=after.jump_url)
        embed.add_field(name="수정된 시각", value=f"<t:{datetime_to_unix(after.edited_at+timedelta(hours=9))}:R>")
        await channel.send(embed=embed)

    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        channel = await self.fetch_channel(LOGGING)
        embed = discord.Embed(title="메세지 삭제됨", color=BAD)
        embed.add_field(name="내용", value=f"```{message.content}```")
        embed.add_field(name="보낸 유저", value=message.author.mention)
        embed.add_field(name="채널", value=message.channel.mention)
        await channel.send(embed=embed)
