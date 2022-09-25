from discord.ext import commands
from flask import Flask
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__, template_folder='templates', static_folder='static')


class Web(commands.Cog):
    def __init__(self):
        app.run()
        
    @app.get("/")
    def root():
        return "hi"


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Web())


def teardown():
    logger.info("Unloaded")