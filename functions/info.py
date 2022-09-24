from discord.ext import commands
import discord
from utils.commands import slash_command
from utils.timeconvert import datetime_to_unix
from discord.commands import ApplicationContext, Option
from config import COLOR
import logging

logger = logging.getLogger(__name__)


class Info(commands.Cog):
    @slash_command(name="유저정보", description="유저의 정보를 전송합니다.")
    async def userinfo(
        self,
        ctx: ApplicationContext,
        user: Option(
            discord.Member, required=False, name="유저", description="정보를 출력할 유저를 입력하세요, 자신을 원한다면 비워두세요."
        )
    ):
        if user is None:
            user = ctx.author
        if user.color == discord.Colour.default():
            embed = discord.Embed(colour=COLOR, title=user.display_name)
        else:
            embed = discord.Embed(colour=user.color, title=str(user))
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="계정명", value=str(user))
        embed.add_field(name="닉네임", value=user.display_name)
        embed.add_field(name="ID", value=str(user.id))
        embed.add_field(name="최상위 역할", value=str(user.top_role))
        if user.bot:
            type_of_user = "봇"
        else:
            type_of_user = "유저"
        embed.add_field(name="유형", value=type_of_user)
        embed.add_field(name="계정 생성 날짜", value=f"<t:{datetime_to_unix(user.created_at)}:R> ({user.created_at})")
        await ctx.respond(embed=embed)

    @slash_command(name="서버정보", description="현재 서버의 정보를 전송합니다.")
    async def serverinfo(self, ctx: ApplicationContext):
        server = ctx.guild
        embed = discord.Embed(colour=COLOR, title=server.name)
        embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name="소유자", value=f"{server.owner.display_name}({str(server.owner)})")
        a = 0
        b = 0
        async for x in server.fetch_members():
            if x.bot:
                b += 1
            else:
                a += 1
        embed.add_field(name="멤버 수", value=f"유저:{a}명, 봇:{b}개")
        embed.add_field(name="ID", value=str(server.id))
        embed.add_field(name="역할 개수", value=str(len(server.roles)))
        embed.add_field(name="서버 생성 날짜", value=f"<t:{datetime_to_unix(server.created_at)}:R> ({server.created_at})")
        await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Info())


def teardown():
    logger.info("Unloaded")
