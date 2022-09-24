import discord
from discord.ext import commands
import os
from time import time
import logging
from utils.logger import setup_logging
from config import TEST_GUILD_ID, STATUS


class JBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None, debug_guilds=[TEST_GUILD_ID])
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.start_time = time()
        for filename in os.listdir("functions"):
            if filename.endswith(".py"):
                self.load_cog(f"functions.{filename[:-3]}")
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
