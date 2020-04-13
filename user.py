import discord
from discord.ext import commands
import configparser
import requests
import json
import ranks

import ereputils

# Config reader
config = configparser.ConfigParser()
config.read("config.ini")

# API Key
apiKey = config["DEFAULT"]["api_key"]
apiVersion = config["DEFAULT"]["api_version"]


class User(commands.Cog, name="User"):
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (commands.ArgumentParsingError)):
            await ctx.send(error)

    async def find_user(self, ctx, in_value):
        user_text = ""
        citizen = ""
        if self.utils.is_number(in_value):
            user_id = str(int(in_value))
            try:
                r = requests.get(
                    "https://api.erepublik.tools/"
                    + apiVersion
                    + "/citizen/"
                    + user_id
                    + "?key="
                    + apiKey
                )
                obj = json.loads(r.text)
                citizen = obj["citizen"]
            except:
                raise commands.ArgumentParsingError("Citizen not found")
        else:
            r = requests.get(
                "https://api.erepublik.tools/v0/citizen?name="
                + in_value
                + "&page=1"
                + "&key="
                + apiKey
            )
            obj = json.loads(r.text)
            pagination = obj["pagination"]
            if pagination["resultsTotal"] == 1:
                user_id = obj["citizen"][0]["id"]
                r = requests.get(
                    "https://api.erepublik.tools/"
                    + apiVersion
                    + "/citizen/"
                    + str(user_id)
                    + "?key="
                    + apiKey
                )
                obj = json.loads(r.text)
                citizen = obj["citizen"]
            else:
                if 1 < pagination["resultsTotal"] <= 9:
                    number_of_matches = 1
                    for citizen_data in obj["citizen"]:
                        user_text += (
                            str(number_of_matches)
                            + ") **"
                            + citizen_data["name"]
                            + "** - *"
                            + str(citizen_data["id"])
                            + "*\n"
                        )
                        number_of_matches += 1
                    em = discord.Embed(
                        title="Please enter the number of the targeted citizen",
                        description=user_text,
                        colour=0x3D9900,
                    )
                    await ctx.message.channel.send("", embed=em)

                    def wait_reply(m):
                        return (
                            m.author == ctx.message.author
                            and m.channel == ctx.message.channel
                        )

                    msg = await self.bot.wait_for(
                        "message", check=wait_reply, timeout=20.0
                    )
                    if int(msg.content) >= number_of_matches or int(msg.content) < 1:
                        await ctx.message.channel.send("Invalid choice")
                        return
                    user_id = int(obj["citizen"][int(msg.content) - 1]["id"])
                    r = requests.get(
                        "https://api.erepublik.tools/"
                        + apiVersion
                        + "/citizen/"
                        + str(user_id)
                        + "?key="
                        + apiKey
                    )
                    obj = json.loads(r.text)
                    citizen = obj["citizen"]
                else:
                    if pagination["resultsTotal"] > 9:
                        user_text += (
                            "***"
                            + in_value
                            + "*** yields too many results (*"
                            + str(pagination["resultsTotal"])
                            + "*).\nPlease specify a more precise username"
                        )
                    if pagination["resultsTotal"] == 0:
                        user_text += (
                            "***" + in_value + "*** doesn't match any known citizens."
                        )

                    em = discord.Embed(
                        title="Citizen information",
                        description=user_text,
                        colour=0x3D9900,
                    )
                    await ctx.message.channel.send("", embed=em)
                    return
        return citizen

    @commands.command(pass_context=True, aliases=["USER"])
    async def user(self, ctx, *, in_value):
        """Returns information for the queried user. Input can be ID or username"""
        citizen = await self.find_user(ctx, in_value)

        embed = discord.Embed(colour=discord.Colour(0xF5A623))
        embed.set_thumbnail(
            url="https://avatar.erepublik.tools/citizen/" + str(citizen["id"]) + ".jpg"
        )
        embed.set_author(
            name=citizen["name"],
            url="https://www.erepublik.com/en/citizen/profile/" + str(citizen["id"]),
            icon_url="https://avatar.erepublik.tools/citizen/"
            + str(citizen["id"])
            + ".jpg",
        )
        embed.set_footer(
            text="Powered by https://erepublik.tools/en",
            icon_url="https://erepublik.tools/assets/img/icon76.png",
        )

        embed.add_field(
            name="Status",
            value=("Alive" if citizen["is_alive"] else "Dead"),
            inline=True,
        )
        embed.add_field(
            name="Date registered",
            value=citizen["registered"]["date"][:10],
            inline=True,
        )
        embed.add_field(name="ID", value=str(citizen["id"]), inline=True)
        embed.add_field(name="Level", value=str(citizen["level"]), inline=True)
        embed.add_field(name="Division", value=str(citizen["division"]), inline=True)
        embed.add_field(
            name="Citizenship",
            value=self.utils.get_country_flag(citizen["citizenship_country_id"])
            + " "
            + citizen["citizenship_country_name"],
            inline=True,
        )
        if citizen["mu_name"]:
            embed.add_field(
                name="Military Unit",
                value="["
                + citizen["mu_name"]
                + "](https://www.erepublik.com/en/military/military-unit/"
                + str(citizen["mu_id"])
                + ")",
                inline=True,
            )
        if citizen["party_name"]:
            embed.add_field(
                name="Party",
                value="["
                + citizen["party_name"]
                + "](https://www.erepublik.com/en/party/"
                + str(citizen["party_id"])
                + ")",
                inline=True,
            )
        embed.add_field(name="Strength", value=str(citizen["strength"]), inline=True)
        embed.add_field(
            name="Perception", value=str(citizen["perception"]), inline=True
        )
        embed.add_field(
            name="Rank",
            value=str(ranks.RANKS_GROUND[citizen["rank_level"] - 1]).replace("*", "\*"),
            inline=True,
        )
        embed.add_field(
            name="Aircraft rank",
            value=str(ranks.RANKS_AIR[citizen["rank_level_aircraft"] - 1]).replace(
                "*", "\*"
            ),
            inline=True,
        )
        if citizen["newspaper_name"]:
            embed.add_field(
                name="Newspaper",
                value="["
                + citizen["newspaper_name"]
                + "](https://www.erepublik.com/en/newspaper/"
                + str(citizen["newspaper_id"])
                + ")",
                inline=True,
            )

        await ctx.message.channel.send("", embed=embed)

    @commands.group(pass_context=True, aliases=["HISTORY"], enabled=False)
    async def history(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.channel.send("Invalid history command passed...")

    @history.command(pass_context=True, aliases=["CS"])
    async def cs(self, ctx, *, in_value: str):
        user_text = ["", "", "", ""]

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get(
            "https://api.erepublik-deutschland.de/"
            + apiKey
            + "/players/history/cs/"
            + found_user[0]
        )
        obj = json.loads(r.text)
        user_text[0] = ""
        i = 0
        hists = obj["history"][found_user[0]]["cs"]

        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x["added"])
            for hist in hists:
                user_text[i] += (
                    self.utils.get_country_flag(hist["country_id_from"])
                    + " ***"
                    + hist["country_name_from"]
                    + "*** to "
                    + self.utils.get_country_flag(hist["country_id_to"])
                    + " ***"
                    + hist["country_name_to"]
                    + "*** on "
                    + hist["added"]
                    + "\n"
                )
                if len(user_text[i]) > 1800:
                    user_text[i] += "..."
                    i += 1
        else:
            user_text[0] = "No history to display."

        embed = discord.Embed(colour=discord.Colour(0xF5A623))
        embed.set_thumbnail(
            url="https://erepublik.tools/avatar/citizen/" + str(found_user[0]) + ".jpg"
        )
        embed.set_author(
            name=str(found_user[1]),
            url="https://www.erepublik.com/en/citizen/profile/" + str(found_user[0]),
            icon_url="https://erepublik.tools/avatar/citizen/"
            + str(found_user[0])
            + ".jpg",
        )
        embed.set_footer(
            text="Powered by https://www.erepublik-deutschland.de/en",
            icon_url="https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png",
        )

        i = 0
        while len(user_text[i]):
            embed.description = user_text[i]
            await ctx.message.channel.send("", embed=embed)
            i += 1

    @history.command(pass_context=True, aliases=["NAME"])
    async def name(self, ctx, *, in_value: str):
        user_text = ["", "", "", ""]

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get(
            "https://api.erepublik-deutschland.de/"
            + apiKey
            + "/players/history/name/"
            + found_user[0]
        )
        obj = json.loads(r.text)
        user_text[0] = ""
        i = 0
        hists = obj["history"][found_user[0]]["name"]
        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x["added"])
            for hist in hists:
                user_text[i] += (
                    "***"
                    + hist["name_from"]
                    + "*** to ***"
                    + hist["name_to"]
                    + "*** on "
                    + hist["added"]
                    + "\n"
                )
                if len(user_text[i]) > 1800:
                    user_text[i] += "..."
                    i += 1
        else:
            user_text[0] = "No history to display."

        embed = discord.Embed(colour=discord.Colour(0xF5A623))
        embed.set_thumbnail(
            url="https://erepublik.tools/avatar/citizen/" + str(found_user[0]) + ".jpg"
        )
        embed.set_author(
            name=str(found_user[1]),
            url="https://www.erepublik.com/en/citizen/profile/" + str(found_user[0]),
            icon_url="https://erepublik.tools/avatar/citizen/"
            + str(found_user[0])
            + ".jpg",
        )
        embed.set_footer(
            text="Powered by https://www.erepublik-deutschland.de/en",
            icon_url="https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png",
        )

        i = 0
        while len(user_text[i]):
            embed.description = user_text[i]
            await ctx.message.channel.send("", embed=embed)
            i += 1

    @history.command(pass_context=True, aliases=["MU"])
    async def mu(self, ctx, *, in_value: str):
        user_text = ["", "", "", ""]

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get(
            "https://api.erepublik-deutschland.de/"
            + apiKey
            + "/players/history/mu/"
            + found_user[0]
        )
        obj = json.loads(r.text)
        user_text[0] = ""
        i = 0
        hists = obj["history"][found_user[0]]["mu"]
        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x["added"])
            for hist in hists:
                user_text[i] += "From " + (
                    "["
                    + hist["mu_name_from"]
                    + "](https://www.erepublik.com/en/military/military-unit/"
                    + str(hist["mu_id_from"])
                    + ")"
                    if hist["mu_name_from"] is not None
                    else "***None***"
                )
                user_text[i] += " to " + (
                    "["
                    + hist["mu_name_to"]
                    + "](https://www.erepublik.com/en/military/military-unit/"
                    + str(hist["mu_id_to"])
                    + ")"
                    if hist["mu_name_to"] is not None
                    else "***None***"
                )
                user_text[i] += " (" + hist["added"] + ")\n"
                if len(user_text[i]) > 1800:
                    user_text[i] += "..."
                    i += 1
        else:
            user_text[0] = "No history to display."

        embed = discord.Embed(colour=discord.Colour(0xF5A623))
        embed.set_thumbnail(
            url="https://erepublik.tools/avatar/citizen/" + str(found_user[0]) + ".jpg"
        )
        embed.set_author(
            name=str(found_user[1]),
            url="https://www.erepublik.com/en/citizen/profile/" + str(found_user[0]),
            icon_url="https://erepublik.tools/avatar/citizen/"
            + str(found_user[0])
            + ".jpg",
        )
        embed.set_footer(
            text="Powered by https://www.erepublik-deutschland.de/en",
            icon_url="https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png",
        )

        i = 0
        while len(user_text[i]):
            embed.description = user_text[i]
            await ctx.message.channel.send("", embed=embed)
            i += 1

    @history.command(pass_context=True, aliases=["PARTY"])
    async def party(self, ctx, *, in_value: str):
        user_text = ["", "", "", ""]

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get(
            "https://api.erepublik-deutschland.de/"
            + apiKey
            + "/players/history/party/"
            + found_user[0]
        )
        obj = json.loads(r.text)
        user_text[0] = ""
        i = 0
        hists = obj["history"][found_user[0]]["party"]
        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x["added"])
            for hist in hists:
                user_text[i] += "From " + (
                    "["
                    + hist["party_name_from"]
                    + "](https://www.erepublik.com/en/party/"
                    + str(hist["party_id_from"])
                    + ")"
                    if hist["party_name_from"] is not None
                    else "***None***"
                )
                user_text[i] += " to " + (
                    "["
                    + hist["party_name_to"]
                    + "](https://www.erepublik.com/en/party/"
                    + str(hist["party_id_to"])
                    + ")"
                    if hist["party_name_to"] is not None
                    else "***None***"
                )
                user_text[i] += " (" + hist["added"] + ")\n"

                if len(user_text[i]) > 1800:
                    user_text[i] += "..."
                    i += 1
        else:
            user_text[0] = "No history to display."

        embed = discord.Embed(colour=discord.Colour(0xF5A623))
        embed.set_thumbnail(
            url="https://erepublik.tools/avatar/citizen/" + str(found_user[0]) + ".jpg"
        )
        embed.set_author(
            name=str(found_user[1]),
            url="https://www.erepublik.com/en/citizen/profile/" + str(found_user[0]),
            icon_url="https://erepublik.tools/avatar/citizen/"
            + str(found_user[0])
            + ".jpg",
        )
        embed.set_footer(
            text="Powered by https://www.erepublik-deutschland.de/en",
            icon_url="https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png",
        )

        i = 0
        while len(user_text[i]):
            embed.description = user_text[i]
            await ctx.message.channel.send("", embed=embed)
            i += 1


def setup(bot):
    bot.add_cog(User(bot))
