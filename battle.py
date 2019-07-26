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


class Battle:
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.group(pass_context=True, aliases=["BATTLE"])
    async def battle(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Invalid battle command passed...")

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
        await self.bot.send_message(ctx.message.channel, "", embed=em)

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
        await self.bot.send_message(ctx.message.channel, "", embed=em)


def setup(bot):
    bot.add_cog(Battle(bot))
