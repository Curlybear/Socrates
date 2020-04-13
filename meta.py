from discord.ext import commands
import discord
from collections import OrderedDict, deque, Counter
import os, datetime
import asyncio
import copy
import unicodedata
import inspect
import itertools
from typing import Union

from paginator import Pages
import ereputils


class HelpPaginator(Pages):
    def __init__(self, help_command, ctx, entries, *, per_page=4):
        super().__init__(ctx, entries=entries, per_page=per_page)
        self.reaction_emojis.append(
            ("\N{WHITE QUESTION MARK ORNAMENT}", self.show_bot_help)
        )
        self.total = len(entries)
        self.help_command = help_command
        self.prefix = help_command.clean_prefix
        self.is_bot = False

    def get_bot_page(self, page):
        cog, description, commands = self.entries[page - 1]
        self.title = f"{cog} Commands"
        self.description = description
        return commands

    def prepare_embed(self, entries, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = self.description
        self.embed.title = self.title

        if self.is_bot:
            value = "For more help, join the official bot support server: https://discord.gg/TX6aqrZ"
            self.embed.add_field(name="Support", value=value, inline=False)

        self.embed.set_footer(
            text=f'Use "{self.prefix}help command" for more info on a command.'
        )

        for entry in entries:
            signature = f"{entry.qualified_name} {entry.signature}"
            self.embed.add_field(
                name=signature, value=entry.short_doc or "No help given", inline=False
            )

        if self.maximum_pages:
            self.embed.set_author(
                name=f"Page {page}/{self.maximum_pages} ({self.total} commands)"
            )

    async def show_help(self):
        """shows this message"""

        self.embed.title = "Paginator help"
        self.embed.description = "Hello! Welcome to the help page."

        messages = [f"{emoji} {func.__doc__}" for emoji, func in self.reaction_emojis]
        self.embed.clear_fields()
        self.embed.add_field(
            name="What are these reactions for?",
            value="\n".join(messages),
            inline=False,
        )

        self.embed.set_footer(
            text=f"We were on page {self.current_page} before this message."
        )
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def show_bot_help(self):
        """shows how to use the bot"""

        self.embed.title = "Using the bot"
        self.embed.description = "Hello! Welcome to the help page."
        self.embed.clear_fields()

        entries = (
            ("<argument>", "This means the argument is __**required**__."),
            ("[argument]", "This means the argument is __**optional**__."),
            ("[A|B]", "This means the it can be __**either A or B**__."),
            (
                "[argument...]",
                "This means you can have multiple arguments.\n"
                "Now that you know the basics, it should be noted that...\n"
                "__**You do not type in the brackets!**__",
            ),
        )

        self.embed.add_field(
            name="How do I use this bot?",
            value="Reading the bot signature is pretty simple.",
        )

        for name, value in entries:
            self.embed.add_field(name=name, value=value, inline=False)

        self.embed.set_footer(
            text=f"We were on page {self.current_page} before this message."
        )
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())


class PaginatedHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "cooldown": commands.Cooldown(1, 3.0, commands.BucketType.member),
                "help": "Shows help about the bot, a command, or a category",
            }
        )

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or "\u200bNo Category"

        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True, key=key)
        nested_pages = []
        per_page = 9
        total = 0

        for cog, commands in itertools.groupby(entries, key=key):
            commands = sorted(commands, key=lambda c: c.name)
            if len(commands) == 0:
                continue

            total += len(commands)
            actual_cog = bot.get_cog(cog)
            # get the description if it exists (and the cog is valid) or return Empty embed.
            description = (actual_cog and actual_cog.description) or discord.Embed.Empty
            nested_pages.extend(
                (cog, description, commands[i : i + per_page])
                for i in range(0, len(commands), per_page)
            )

        # a value of 1 forces the pagination session
        pages = HelpPaginator(self, self.context, nested_pages, per_page=1)

        # swap the get_page implementation to work with our nested pages.
        pages.get_page = pages.get_bot_page
        pages.is_bot = True
        pages.total = total
        await pages.paginate()

    async def send_cog_help(self, cog):
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        pages = HelpPaginator(self, self.context, entries)
        pages.title = f"{cog.qualified_name} Commands"
        pages.description = cog.description

        await pages.paginate()

    def common_command_formatting(self, page_or_embed, command):
        page_or_embed.title = self.get_command_signature(command)
        if command.description:
            page_or_embed.description = f"{command.description}\n\n{command.help}"
        else:
            page_or_embed.description = command.help or "No help found..."

    async def send_command_help(self, command):
        # No pagination necessary for a single command.
        embed = discord.Embed(colour=discord.Colour.blurple())
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        pages = HelpPaginator(self, self.context, entries)
        self.common_command_formatting(pages, group)

        await pages.paginate()


class Meta(commands.Cog):
    """Commands for utilities related to Discord or the Bot itself."""

    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = PaginatedHelpCommand()
        bot.help_command.cog = self
        self.utils = ereputils.ErepUtils()

    def cog_unload(self):
        self.bot.help_command = self.old_help_command

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument, commands.ArgumentParsingError):
            await ctx.send(error)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pings the bot"""
        em = discord.Embed(
            title="Pong", description=ctx.message.content, colour=0x3D9900
        )
        await ctx.message.channel.send("", embed=em)

    @commands.command(pass_context=True, aliases=["CONVERT"])
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
            raise commands.ArgumentParsingError(
                "Invalid input. Expected format is erep day or date (dd/mm/yyyy)"
            )

    @commands.command(pass_context=True, aliases=["INVITE"])
    async def invite(self, ctx):
        """Return the link to invite Socrates to your own server"""
        await ctx.message.channel.send(
            "To invite me to your own server click the following link: <https://discordapp.com/oauth2/authorize?client_id=304725683995934723&scope=bot&permissions=0>"
        )

    @commands.command(
        pass_context=True, aliases=["INTHEFOLLOWINGWEEKS", "itfw", "ITFW"]
    )
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
        await ctx.message.channel.send("", embed=em)

    @commands.command(pass_context=True)
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
            value="https://discordapp.com/oauth2/authorize?client_id=304725683995934723&scope=bot&permissions=0",
            inline=True,
        )
        embed.set_footer(
            text="Curlybear#7847", icon_url="https://i.imgur.com/Umqjr4M.png"
        )
        embed.set_thumbnail(url="https://i.imgur.com/1ZBsqym.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Meta(bot))
