from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from config import REGISTER
import logging

logger = logging.getLogger(__name__)


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="신청", description="대회 참가 신청을 합니다.")
    async def register(
        self,
        ctx: ApplicationContext,
        num: Option(int, name="학번", description="학번을 입력하세요."),
        name: Option(str, name="이름", description="이름을 입력하세요")
    ):
        channel = await self.bot.fetch_channel(REGISTER)
        await channel.send(f"{num} {name} | 참가신청 완료")
        await ctx.respond("참가신청이 완료되었습니다.")


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Register(bot))


def teardown():
    logger.info("Unloaded")
