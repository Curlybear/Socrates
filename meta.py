from discord.ext import commands
import discord
from discord import app_commands
from collections import OrderedDict, deque, Counter
import os, datetime
import asyncio
import copy
import unicodedata
import inspect
import itertools
from typing import Union

import ereputils

class Meta(commands.Cog):
    """Commands for utilities related to Discord or the Bot itself."""

    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (commands.BadArgument, commands.ArgumentParsingError)):
            await ctx.send(error)

    @commands.hybrid_command(name="ping", )
    async def ping(self, ctx: commands.Context) -> None:
        """Pings the bot"""
        await ctx.send("Pong")

    @commands.hybrid_command(name="convert")
    async def convert(self, ctx, in_value: str):
        """Return the conversion of the provided erepDay or date (dd/mm/yyyy)"""
        start_date = datetime.datetime(day=21, month=11, year=2007)
        try:
            if self.utils.is_number(in_value):
                delta = datetime.timedelta(days=int(in_value) - 1)
                final_date = start_date + delta
                em = discord.Embed(
                    title="Conversion",
                    description="Date : " + final_date.strftime("%d/%m/%Y"),
                    colour=0x0053A9,
                )
                await ctx.send("", embed=em)
            else:
                in_date = datetime.datetime.strptime(in_value, "%d/%m/%Y")
                erep_day = in_date - start_date + datetime.timedelta(days=1)
                em = discord.Embed(
                    title="Conversion",
                    description="eRepublik day : " + str(erep_day.days),
                    colour=0x0053A9,
                )
                await ctx.send("", embed=em)
        except:
            raise commands.ArgumentParsingError(
                "Invalid input. Expected format is erep day or date (dd/mm/yyyy)"
            )

    @commands.hybrid_command(name="invite")
    async def invite(self, ctx):
        """Return the link to invite Socrates to your own server"""
        await ctx.send(
            "To invite me to your own server click the following link: <https://discord.com/api/oauth2/authorize?client_id=304725683995934723&permissions=2147485760&scope=applications.commands%20bot>"
        )

    @commands.hybrid_command(name="itfw")
    async def inthefollowingweeks(self, ctx):
        """In the following weeks..."""
        rip_date = datetime.datetime(2017, 5, 19, 13, 38)
        elapsed_time = datetime.datetime.utcnow() - rip_date
        em = discord.Embed(
            title="In the following weeks",
            description='"The local elections module will be added as the next step in the following weeks."',
            colour=0x0053A9,
        )
        em.add_field(
            name="Time elapsed since then",
            value=str(elapsed_time.days)
            + " days, "
            + str(elapsed_time.seconds // 3600)
            + " hours, "
            + str((elapsed_time.seconds // 60) % 60)
            + " minutes",
            inline=False,
        )
        em.set_author(
            name="Curlybear#1962",
            url="https://curlybear.eu",
            icon_url="https://erpk-static-avatars.s3.amazonaws.com/avatars/Citizens/2011/07/12/0a83af20636fe1ac4d01c6d132572943.png?8e8837b38eeff670f9301b95d31a47a2",
        )
        em.set_footer(
            text="Powered by https://www.erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        await ctx.send("", embed=em)

    @commands.hybrid_command(name="botinfo", pass_context=True)
    async def botinfo(self, ctx):
        """Returns basic information about Socrates"""
        embed = discord.Embed(title="Socrates Info", color=0xA9152B)
        embed.add_field(
            name="Uptime",
            value=str(datetime.datetime.now() - self.bot.uptimeStart)[:-7],
            inline=True,
        )
        embed.add_field(name="Created On", value="2017-04-19", inline=True)
        embed.add_field(name="** **", value="** **", inline=True)
        embed.add_field(name="Guilds Serving", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users Serving", value=len(self.bot.users), inline=True)
        embed.add_field(name="** **", value="** **", inline=True)
        embed.add_field(
            name="Bot Invite Link",
            value="https://discord.com/api/oauth2/authorize?client_id=304725683995934723&scope=applications.commands",
            inline=True,
        )
        embed.set_footer(
            text="Curlybear#7847", icon_url="https://i.imgur.com/Umqjr4M.png"
        )
        embed.set_thumbnail(url="https://i.imgur.com/1ZBsqym.png")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Meta(bot))