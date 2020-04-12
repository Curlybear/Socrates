import datetime
import logging
import traceback

import discord
from discord import message
from discord.ext import commands

import check
import ereputils

logger = logging.getLogger("Socrates." + __name__)


class Misc(commands.Cog, name="Misc"):
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.command(pass_context=True, aliases=["PING"])
    async def ping(self, ctx):
        """Pings the bot"""
        logger.info("!ping - User: " + str(ctx.message.author))
        em = discord.Embed(
            title="Pong", description=ctx.message.content, colour=0x3D9900
        )
        await ctx.message.channel.send("", embed=em)

    @commands.command(pass_context=True, aliases=["HELP"])
    async def help(self, ctx):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        em = discord.Embed(
            title="Help", description="Available commands", colour=0x0053A9
        )
        em.add_field(
            name="!alliances",
            value="Return a visual representation of the alliances",
            inline=False,
        )
        em.add_field(
            name="!convert [erepDay|date]",
            value="Return the conversion of the provided erepDay or date (dd/mm/yyyy)",
            inline=False,
        )
        em.add_field(name="!help", value="Return this help message", inline=False)
        em.add_field(
            name="!invite",
            value="Return the link to invite Socrates to your own server",
            inline=False,
        )
        em.add_field(
            name="!(food|weapons|aircrafts|houses|tickets|frm|wrm|arm|hrm) [quality]",
            value="Returns a list of the best offers for the given product",
        )
        em.add_field(
            name="!jobs [country]",
            value="Returns the top jobs of a given country, overall if none or provided",
            inline=False,
        )
        em.add_field(
            name="!mpp [country]",
            value="Returns the mpp list for the given country",
            inline=False,
        )
        em.add_field(
            name="!user [username|userid]",
            value="Return the information regarding a specified user",
            inline=False,
        )
        em.add_field(
            name="!rh [country]",
            value="Return the list of occupied regions of a given country",
            inline=False,
        )
        em.add_field(
            name="!sh",
            value="Return the list of the upcoming air rounds as well as air rounds with limited damage done",
            inline=False,
        )
        em.add_field(
            name="!wiki [entry name]",
            value="Return the information relative to the queried entry",
            inline=False,
        )
        em.add_field(
            name="!wikicats",
            value="Return the categories available in the wiki",
            inline=False,
        )
        em.add_field(
            name="!wikilist [category]",
            value="Return the list of entries belonging to a given category",
            inline=False,
        )
        em.set_author(
            name="Curlybear#1962",
            url="https://curlybear.eu",
            icon_url="https://erpk-static-avatars.s3.amazonaws.com/avatars/Citizens/2011/07/12/0a83af20636fe1ac4d01c6d132572943.png?8e8837b38eeff670f9301b95d31a47a2",
        )
        em.set_thumbnail(url="http://www.dipsacademy.com/images/socrates.png")
        em.set_footer(
            text="Powered by https://www.erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        await ctx.message.channel.send("", embed=em)

    @commands.command(pass_context=True, aliases=["CONVERT"])
    async def convert(self, ctx, in_value: str):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))

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
                await ctx.message.channel.send("", embed=em)
            else:
                in_date = datetime.datetime.strptime(in_value, "%d/%m/%Y")
                erep_day = in_date - start_date + datetime.timedelta(days=1)
                em = discord.Embed(
                    title="Conversion",
                    description="eRepublik day : " + str(erep_day.days),
                    colour=0x0053A9,
                )
                await ctx.message.channel.send("", embed=em)
        except:
            traceback.print_exc()
            logger.info("   Invalid input")
            await self.bot.say("Invalid input")

    @commands.command(pass_context=True, aliases=["INVITE"])
    async def invite(self, ctx):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        await ctx.message.channel.send(
            "To invite me to your own server click the following link: <https://discordapp.com/oauth2/authorize?client_id=304725683995934723&scope=bot&permissions=0>"
        )

    @commands.command(pass_context=True, aliases=["ANNOUNCEMENT"])
    @check.is_authorized_staff()
    async def announcement(self, ctx, *, message: str):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        for server in self.bot.servers:
            try:
                await ctx.message.channel.send(
                    "\n\nSent by: *" + str(ctx.message.author) + "*"
                )
                logger.info("   Sent to: " + str(server))
            except:
                logger.info("   Not sent to: " + str(server))
                pass

    @commands.command(
        pass_context=True, aliases=["INTHEFOLLOWINGWEEKS", "itfw", "ITFW"]
    )
    async def inthefollowingweeks(self, ctx):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
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
        await ctx.message.channel.send("", embed=em)

    @commands.command(pass_context=True)
    async def botinfo(self, ctx):
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
            value="https://discordapp.com/oauth2/authorize?client_id=304725683995934723&scope=bot&permissions=0",
            inline=True,
        )
        embed.set_footer(
            text="Curlybear#7847", icon_url="https://i.imgur.com/Umqjr4M.png"
        )
        embed.set_thumbnail(url="https://i.imgur.com/1ZBsqym.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
