import discord
from discord.ext import commands
import configparser
import logging
import requests
import json

import ereputils

logger = logging.getLogger("Socrates." + __name__)

# Config reader
config = configparser.ConfigParser()
config.read("config.ini")

# API
apiKey = config["DEFAULT"]["api_key"]
apiVersion = config["DEFAULT"]["api_version"]


class Market(commands.Cog, name="Market"):
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.command(pass_context=True, aliases=["FOOD"])
    async def food(self, ctx, in_quality: str):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return
        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/1/"
            + in_quality
            + "?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best Q" + in_quality + " food offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/1_"
            + in_quality
            + ".png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["WEAPONS"])
    async def weapons(self, ctx, in_quality: str):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/2/"
            + in_quality
            + "?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best Q" + in_quality + " weapons offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/2_"
            + in_quality
            + ".png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["AIRCRAFTS"])
    async def aircrafts(self, ctx, in_quality: str = "1"):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/23/"
            + in_quality
            + "?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best Q" + in_quality + " aircraft offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/23_"
            + in_quality
            + ".png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["HOUSES"])
    async def houses(self, ctx, in_quality: str):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/4/"
            + in_quality
            + "?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best Q" + in_quality + " house offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/4_"
            + in_quality
            + ".png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["TICKETS"])
    async def tickets(self, ctx, in_quality: str):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/3/"
            + in_quality
            + "?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best Q" + in_quality + " ticket offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/3_"
            + in_quality
            + ".png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["FRM"])
    async def frm(self, ctx):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/7/1?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best frm offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/7_1.png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["WRM"])
    async def wrm(self, ctx):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/12/1?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best wrm offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/12_1.png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["HRM"])
    async def hrm(self, ctx):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/17/1?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best hrm offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/17_1.png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)

    @commands.command(pass_context=True, aliases=["ARM"])
    async def arm(self, ctx):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))

        r = requests.get(
            "https://api.erepublik.tools/"
            + apiVersion
            + "/market/item/best-offers/24/1?key="
            + apiKey
        )
        obj = json.loads(r.text)
        offers = obj["offers"]

        countries = ""
        prices = ""
        links = ""
        if not offers:
            await ctx.message.channel.send("No matching offers")
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]["country_id"])
                countries += (
                    flag
                    + " "
                    + self.utils.get_country_name(offers[i]["country_id"])
                    + "\n"
                )
                prices += (
                    ":dollar: "
                    + str(offers[i]["gross"])
                    + " - :package: "
                    + str(offers[i]["amount"])
                    + "\n"
                )
                links += (
                    ":link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/"
                    + str(offers[i]["id"])
                    + ")"
                    + "\n"
                )

        embed = discord.Embed(colour=discord.Colour(0xCE2C19))
        embed.set_author(
            name="Best arm offers",
            icon_url="https://static.erepublik.tools/assets/img/erepublik/industry/24_1.png",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await ctx.message.channel.send("", embed=embed)


def setup(bot):
    bot.add_cog(Market(bot))
