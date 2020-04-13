import discord
from discord.ext import commands
import configparser
import requests
import json
import datetime
from bs4 import BeautifulSoup

import ereputils

# Config reader
config = configparser.ConfigParser()
config.read("config.ini")

# API Key
apiKey = config["DEFAULT"]["api_key"]
apiVersion = config["DEFAULT"]["api_version"]


class Country(commands.Cog, name="Country"):
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (commands.ArgumentParsingError)):
            await ctx.send(error)

    @commands.command(pass_context=True, aliases=["MPP"])
    async def mpp(self, ctx, *, in_country: str):
        try:
            uid = self.utils.get_country_id(in_country)
            country = self.utils.get_country_name(uid)
            mpp_text = ""
            expiration_text = ""
            r = requests.get("http://api.erepublik.com/map/data/")
            e = BeautifulSoup(r.text, "html.parser")

            mpps = e.countries.find(name="country", c_id=uid).mpps
            if mpps.string == " ":
                mpp_text += "**No MPPs**"
                expiration_text += "**No MPPs**"
            else:
                for mpp in sorted(mpps, key=lambda x: x["expires"]):
                    mpp_text += (
                        self.utils.get_country_flag(mpp["c_id"])
                        + " **"
                        + self.utils.get_country_name(mpp["c_id"])
                        + "**"
                        + "\n"
                    )

                    expiration_text += (
                        ":small_blue_diamond: "
                        + mpp["expires"][:4]
                        + "-"
                        + mpp["expires"][4:6]
                        + "-"
                        + mpp["expires"][6:8]
                        + "\n"
                    )

            embed = discord.Embed(colour=discord.Colour(0xCE2C19))
            embed.set_author(
                name=country + " Mutual Protection Pacts",
                icon_url="https://static.erepublik.tools/assets/img/erepublik/country/"
                + str(uid)
                + ".gif",
            )
            embed.set_footer(
                text="Powered by https://erepublik.tools",
                icon_url="https://erepublik.tools/assets/img/icon76.png",
            )
            embed.add_field(name="Country", value=mpp_text, inline=True)
            embed.add_field(name="Expiration date", value=expiration_text, inline=True)
            await ctx.message.channel.send("", embed=embed)
        except:
            raise commands.ArgumentParsingError(
                "Country ***" + in_country + "*** not recognized"
            )

    @commands.command(pass_context=True, aliases=["MPPSRAW"])
    async def mppsraw(self, ctx):
        mpp_text = ""

        r = requests.get("http://api.erepublik.com/map/data/")
        e = BeautifulSoup(r.text, "html.parser")

        for country in e.countries:
            mpps = country.mpps
            if len(mpps.text) == 0:
                for mpp in sorted(mpps, key=lambda x: x["expires"]):
                    mpp_text += (
                        self.utils.get_country_name(country["c_id"])
                        + ";"
                        + self.utils.get_country_name(mpp["c_id"])
                        + ";"
                        + mpp["expires"][6:8]
                        + "/"
                        + mpp["expires"][4:6]
                        + "/"
                        + mpp["expires"][:4]
                        + "\n"
                    )

        with open(
            config["PASTE"]["paste_path"]
            + "mpps"
            + datetime.datetime.now().strftime("%d-%m-%Y")
            + ".csv",
            "w",
        ) as f:
            f.write(mpp_text)
        em = discord.Embed(
            title="All MPPs",
            description=config["PASTE"]["paste_url"]
            + "mpps"
            + datetime.datetime.now().strftime("%d-%m-%Y")
            + ".csv",
            colour=0x0042B9,
        )
        await ctx.message.channel.send("", embed=em)

    @commands.command(pass_context=True, aliases=["CINFO"], enabled=False)
    async def cinfo(self, ctx, *, in_country: str):
        try:
            uid = self.utils.get_country_id(in_country)
            country = self.utils.get_country_name(uid)
            r = requests.get(
                "https://api.erepublik-deutschland.de/"
                + apiKey
                + "/countries/details/"
                + str(uid)
            )
            obj = json.loads(r.text)

            embed = discord.Embed(colour=discord.Colour(0xCE2C19))
            embed.set_author(
                name=country + " Information",
                icon_url="https://static.erepublik.tools/assets/img/erepublik/country/"
                + str(uid)
                + ".gif",
            )
            embed.set_footer(
                text="Powered by https://www.erepublik-deutschland.de/en",
                icon_url="https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png",
            )

            embed.add_field(
                name="Administration",
                value="--------------------------------------",
                inline=False,
            )
            if obj["countries"][str(uid)]["administration"]["dictator"]["id"]:
                embed.add_field(
                    name="Dictator",
                    value="["
                    + obj["countries"][str(uid)]["administration"]["dictator"]["name"]
                    + "](https://www.erepublik.com/en/citizen/profile/"
                    + str(
                        obj["countries"][str(uid)]["administration"]["dictator"]["id"]
                    )
                    + ")",
                    inline=True,
                )
            if obj["countries"][str(uid)]["administration"]["president"]["id"]:
                embed.add_field(
                    name="President",
                    value="["
                    + obj["countries"][str(uid)]["administration"]["president"]["name"]
                    + "](https://www.erepublik.com/en/citizen/profile/"
                    + str(
                        obj["countries"][str(uid)]["administration"]["president"]["id"]
                    )
                    + ")",
                    inline=True,
                )
            for minister in obj["countries"][str(uid)]["administration"]["minister"]:
                embed.add_field(
                    name=minister,
                    value="["
                    + obj["countries"][str(uid)]["administration"]["minister"][
                        minister
                    ]["name"]
                    + "](https://www.erepublik.com/en/citizen/profile/"
                    + str(
                        obj["countries"][str(uid)]["administration"]["minister"][
                            minister
                        ]["id"]
                    )
                    + ")",
                    inline=True,
                )
            embed.add_field(
                name="Finance",
                value="--------------------------------------",
                inline=False,
            )
            embed.add_field(
                name="CC",
                value=str(obj["countries"][str(uid)]["economy"]["cc"]),
                inline=True,
            )
            embed.add_field(
                name="Gold",
                value=str(obj["countries"][str(uid)]["economy"]["gold"]),
                inline=True,
            )
            embed.add_field(
                name="Average salary",
                value=str(obj["countries"][str(uid)]["economy"]["salary_average"])
                + " CC",
                inline=True,
            )
            embed.add_field(
                name="Population",
                value=str(obj["countries"][str(uid)]["population"]["total"])
                + " citizens",
                inline=True,
            )

            await ctx.message.channel.send("", embed=embed)
        except:
            raise commands.ArgumentParsingError(
                "Country ***" + in_country + "*** not recognized"
            )

    @commands.command(pass_context=True)
    async def jobs(self, ctx, *, in_country=None):
        try:
            if in_country:
                uid = self.utils.get_country_id(in_country)
                country = self.utils.get_country_name(uid)
            else:
                uid = "best-offers"
                country = "World"
            r = requests.get(
                "https://api.erepublik.tools/{}/market/job/{}?key={}".format(
                    apiVersion, uid, apiKey
                )
            )
            obj = json.loads(r.text)
            offers = obj["offers"]

            countries = ""
            salary = ""
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
                    salary += (
                        ":dollar: "
                        + str(offers[i]["gross"])
                        + " ("
                        + str(offers[i]["net"])
                        + ") - :moneybag: "
                        + (
                            str(offers[i]["salary_limit"])
                            if str(offers[i]["salary_limit"]) != "0"
                            else "∞"
                        )
                        + "\n"
                    )
                    links += (
                        ":link: [Link to offer](https://www.erepublik.com/en/economy/job-market/"
                        + str(offers[i]["country_id"])
                        + ")"
                        + "\n"
                    )

            embed = discord.Embed(colour=discord.Colour(0xCE2C19))
            title = (
                "Best job offers"
                if not in_country
                else "Best job offers in {}".format(country)
            )
            embed.set_author(name=title)
            embed.set_footer(
                text="Powered by https://erepublik.tools",
                icon_url="https://erepublik.tools/assets/img/icon76.png",
            )
            embed.add_field(name="Country", value=countries, inline=True)
            embed.add_field(name="Salary(net) - Limit", value=salary, inline=True)
            embed.add_field(name="Link", value=links, inline=True)

            await ctx.message.channel.send("", embed=embed)
        except:
            raise commands.ArgumentParsingError(
                "Country ***" + in_country + "*** not recognized"
            )


def setup(bot):
    bot.add_cog(Country(bot))
