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

# API Key
apiKey = config["DEFAULT"]["api_key"]
apiVersion = config["DEFAULT"]["api_version"]


class Battle(commands.Cog, name="Battle"):
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.group(pass_context=True, aliases=["BATTLE"])
    async def battle(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.channel.send("Invalid battle command passed...")

    @battle.command(pass_context=True, aliases=["INFO"])
    async def info(self, ctx, battle_id):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        r = requests.get(
            "https://api.erepublik-deutschland.de/"
            + apiKey
            + "/battles/details/"
            + battle_id
        )
        obj = json.loads(r.text)

        battle_info = obj["details"][battle_id]
        battle_text = ""

        battle_text += (
            "**"
            + battle_info["region"]["name"]
            + "** (Round: "
            + str(battle_info["general"]["round"])
            + ")\n"
        )
        battle_text += (
            self.utils.get_country_flag(battle_info["attacker"]["id"])
            + " **"
            + battle_info["attacker"]["name"]
            + "** [*"
            + str(battle_info["attacker"]["points"])
            + "*] - "
            + self.utils.get_country_flag(battle_info["defender"]["id"])
            + " **"
            + battle_info["defender"]["name"]
            + "** [*"
            + str(battle_info["defender"]["points"])
            + "*]\n"
        )
        battle_text += (
            "**[Division 1]**  ***Wall***: *"
            + str(battle_info["wall"]["1"]["attacker"])[0:5]
            + "* vs *"
            + str(battle_info["wall"]["1"]["defender"])[0:5]
            + "* - ***Domination***: *"
            + str(battle_info["domination"]["1"]["attacker"])
            + "* vs *"
            + str(battle_info["domination"]["1"]["defender"])
            + "*\n"
        )
        battle_text += (
            "**[Division 2]**  ***Wall***: *"
            + str(battle_info["wall"]["2"]["attacker"])[0:5]
            + "* vs *"
            + str(battle_info["wall"]["2"]["defender"])[0:5]
            + "* - ***Domination***: *"
            + str(battle_info["domination"]["2"]["attacker"])
            + "* vs *"
            + str(battle_info["domination"]["2"]["defender"])
            + "*\n"
        )
        battle_text += (
            "**[Division 3]**  ***Wall***: *"
            + str(battle_info["wall"]["3"]["attacker"])[0:5]
            + "* vs *"
            + str(battle_info["wall"]["3"]["defender"])[0:5]
            + "* - ***Domination***: *"
            + str(battle_info["domination"]["3"]["attacker"])
            + "* vs *"
            + str(battle_info["domination"]["3"]["defender"])
            + "*\n"
        )
        battle_text += (
            "**[Division 4]**  ***Wall***: *"
            + str(battle_info["wall"]["4"]["attacker"])[0:5]
            + "* vs *"
            + str(battle_info["wall"]["4"]["defender"])[0:5]
            + "* - ***Domination***: *"
            + str(battle_info["domination"]["4"]["attacker"])
            + "* vs *"
            + str(battle_info["domination"]["4"]["defender"])
            + "*\n"
        )

        battle_text += (
            "**Battle link**: https://www.erepublik.com/en/military/battlefield-new/"
            + str(battle_id)
            + "\n"
        )

        em = discord.Embed(
            title="Battle information (" + battle_id + ")",
            description=battle_text,
            colour=0xBFF442,
        )
        await ctx.message.channel.send("", embed=em)

    @battle.command(pass_context=True, aliases=["CO"])
    async def co(self, ctx, battle_id):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        r = requests.get(
            "https://api.erepublik-deutschland.de/"
            + apiKey
            + "/battles/details/"
            + battle_id
        )
        obj = json.loads(r.text)

        battle_info = obj["details"][battle_id]
        battle_info_co = obj["details"][battle_id]["combat_orders"]
        battle_text = ""

        battle_text += (
            "**"
            + battle_info["region"]["name"]
            + "** (Round: "
            + str(battle_info["general"]["round"])
            + ")\n"
        )
        battle_text += (
            self.utils.get_country_flag(battle_info["attacker"]["id"])
            + " **"
            + battle_info["attacker"]["name"]
            + "** [*"
            + str(battle_info["attacker"]["points"])
            + "*] - "
            + self.utils.get_country_flag(battle_info["defender"]["id"])
            + " **"
            + battle_info["defender"]["name"]
            + "** [*"
            + str(battle_info["defender"]["points"])
            + "*]\n\n"
        )
        if "1" in battle_info_co:
            battle_text += "**[Division 1]**\n"
            if "1" in battle_info_co:
                for co in battle_info_co["1"]:
                    battle_text += (
                        "Side: "
                        + self.utils.get_country_flag(
                            battle_info_co["1"][co]["country"]["id"]
                        )
                        + " **"
                        + battle_info_co["1"][co]["country"]["name"]
                        + "** - Reward: *"
                        + str(battle_info_co["1"][co]["reward"])
                        + "* - Budget: *"
                        + str(battle_info_co["1"][co]["budget"])
                        + "* - Wall: *"
                        + str(battle_info_co["1"][co]["wall"])
                        + "*\n"
                    )
            battle_text += "\n**[Division 2]**\n"
            if "2" in battle_info_co:
                for co in battle_info_co["2"]:
                    battle_text += (
                        "Side: "
                        + self.utils.get_country_flag(
                            battle_info_co["2"][co]["country"]["id"]
                        )
                        + " **"
                        + battle_info_co["2"][co]["country"]["name"]
                        + "** - Reward: *"
                        + str(battle_info_co["2"][co]["reward"])
                        + "* - Budget: *"
                        + str(battle_info_co["2"][co]["budget"])
                        + "* - Wall: *"
                        + str(battle_info_co["2"][co]["wall"])
                        + "*\n"
                    )
            battle_text += "\n**[Division 3]**\n"
            if "3" in battle_info_co:
                for co in battle_info_co["3"]:
                    battle_text += (
                        "Side: "
                        + self.utils.get_country_flag(
                            battle_info_co["3"][co]["country"]["id"]
                        )
                        + " **"
                        + battle_info_co["3"][co]["country"]["name"]
                        + "** - Reward: *"
                        + str(battle_info_co["3"][co]["reward"])
                        + "* - Budget: *"
                        + str(battle_info_co["3"][co]["budget"])
                        + "* - Wall: *"
                        + str(battle_info_co["3"][co]["wall"])
                        + "*\n"
                    )
            battle_text += "\n**[Division 4]**\n"
            if "4" in battle_info_co:
                for co in battle_info_co["4"]:
                    battle_text += (
                        "Side: "
                        + self.utils.get_country_flag(
                            battle_info_co["4"][co]["country"]["id"]
                        )
                        + " **"
                        + battle_info_co["4"][co]["country"]["name"]
                        + "** - Reward: *"
                        + str(battle_info_co["4"][co]["reward"])
                        + "* - Budget: *"
                        + str(battle_info_co["4"][co]["budget"])
                        + "* - Wall: *"
                        + str(battle_info_co["4"][co]["wall"])
                        + "*\n"
                    )
        if "11" in battle_info_co:
            battle_text += "**[Aerial round]**\n"
            for co in battle_info_co["11"]:
                battle_text += (
                    "Side: "
                    + self.utils.get_country_flag(
                        battle_info_co["11"][co]["country"]["id"]
                    )
                    + " **"
                    + battle_info_co["11"][co]["country"]["name"]
                    + "** - Reward: *"
                    + str(battle_info_co["11"][co]["reward"])
                    + "* - Budget: *"
                    + str(battle_info_co["11"][co]["budget"])
                    + "* - Wall: *"
                    + str(battle_info_co["11"][co]["wall"])
                    + "*\n"
                )
        battle_text += (
            "\n**Battle link**: https://www.erepublik.com/en/military/battlefield-new/"
            + str(battle_id)
            + "\n"
        )

        em = discord.Embed(
            title="Battle co information (" + battle_id + ")",
            description=battle_text,
            colour=0xBFF442,
        )
        await ctx.message.channel.send("", embed=em)

    @commands.command(pass_context=True, aliases=["RH"])
    async def rh(self, ctx, *, in_country):
        logger.info(ctx.message.content + " - User: " + str(ctx.message.author))
        try:
            if in_country != "World":
                uid = self.utils.get_country_id(in_country)
                country = self.utils.get_country_name(uid)
            region_text = ""
            time_text = ""
            occupied_text = ""
            count = 0
            r = requests.get(
                "https://api.erepublik.tools/"
                + apiVersion
                + "/region/list?key="
                + apiKey
            )
            obj = json.loads(r.text)
            regions = obj["regions"]

            for region in regions:
                if region["original_owner_country_id"] == uid and region.get(
                    "under_occupation_since"
                ):
                    if count < 10:
                        region_text += (
                            self.utils.get_country_flag(
                                region["original_owner_country_id"]
                            )
                            + " **"
                            + region["name"]
                            + "**"
                            + "\n"
                        )
                        time_text += (
                            ":small_blue_diamond: "
                            + region["under_occupation_since"]["date"][:-7]
                            + "\n"
                        )
                        occupied_text += (
                            ":small_orange_diamond: "
                            + self.utils.get_country_flag(
                                region["current_owner_country_id"]
                            )
                            + " "
                            + self.utils.get_country_name(
                                region["current_owner_country_id"]
                            )
                            + "\n"
                        )
                    count = count + 1
            if count:
                region_text = (
                    region_text + "\n**Total occupied regions: **" + str(count)
                )

            embed = discord.Embed(colour=discord.Colour(0xCE2C19))
            embed.set_author(
                name=country + " RHs",
                icon_url="https://static.erepublik.tools/assets/img/erepublik/country/"
                + str(uid)
                + ".gif",
            )
            embed.set_footer(
                text="Powered by https://erepublik.tools",
                icon_url="https://erepublik.tools/assets/img/icon76.png",
            )
            if region_text == "":
                embed.add_field(
                    name="Regions",
                    value="No regions under occupation are held by " + country,
                    inline=True,
                )
            else:
                embed.add_field(name="Regions", value=region_text, inline=True)
                embed.add_field(
                    name="Under occupation since", value=time_text, inline=True
                )
                embed.add_field(name="Occupied by", value=occupied_text, inline=True)
            await ctx.message.channel.send("", embed=embed)
        except:
            logger.info("\tCountry ***" + in_country + "*** not recognized")
            await ctx.message.channel.send(
                "Country ***" + in_country + "*** not recognized"
            )


def setup(bot):
    bot.add_cog(Battle(bot))
