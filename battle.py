import configparser
import json
from os.path import join

import discord
import requests
from discord.ext import commands

import ereputils

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

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (commands.ArgumentParsingError)):
            await ctx.send(error)

    @commands.hybrid_command(aliases=["RH"])
    async def rh(self, ctx, *, country):
        """Returns the list of occupied regions of a given country"""
        try:
            if country != "World":
                uid = self.utils.get_country_id(country)
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
            picked_regions = list()
            for region in regions:
                if (
                    region["original_owner_country_id"] == uid
                    or region["current_owner_country_id"] == uid
                ) and region.get("under_occupation_since"):
                    picked_regions.append(region)

            picked_regions.sort(
                key=lambda region: region["under_occupation_since"]["date"],
                reverse=True,
            )

            for region in picked_regions:
                if count < 20:
                    region_text += (
                        self.utils.get_country_flag(region["original_owner_country_id"])
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
                    country_name = self.utils.get_country_name(
                        region["current_owner_country_id"]
                    )
                    country_name = (
                        (country_name[:17] + "..")
                        if len(country_name) > 17
                        else country_name
                    )
                    occupied_text += (
                        ":small_orange_diamond: "
                        + self.utils.get_country_flag(
                            region["current_owner_country_id"]
                        )
                        + " "
                        + country_name
                        + "\n"
                    )
                    count = count + 1
            if count:
                region_text = (
                    region_text
                    + "\n**Total occupied regions: **"
                    + str(len(picked_regions))
                )
                if count < len(picked_regions):
                    region_text = region_text + " ({} not displayed)".format(
                        len(picked_regions) - count
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
            await ctx.send("", embed=embed)
        except:
            raise commands.ArgumentParsingError(
                "Country ***" + country + "*** not recognized"
            )

    @commands.hybrid_command(aliases=["SH"])
    async def sh(self, ctx):
        """Returns the list of the upcoming air rounds as well as air rounds with limited damage done."""
        r = requests.get("https://www.erepublik.com/en/military/campaignsJson/list")
        data = json.loads(r.text)
        battles = data["battles"]
        picked_battles = list()
        for battle_id in battles:
            battle = battles[battle_id]
            if battle["type"] == "aircraft":
                battle["delay"] = battle["start"] - data["time"]
                if battle["delay"] > 0:
                    picked_battles.append(battle)
                else:
                    battle["started_since"] = data["time"] - battle["start"]

                    div_id = next(iter(battle["div"]))
                    if battle["div"][div_id]["stats"]["inv"]:
                        battle["inv_damage"] = battle["div"][div_id]["stats"]["inv"][
                            "damage"
                        ]
                    else:
                        battle["inv_damage"] = 0
                    if battle["div"][div_id]["stats"]["def"]:
                        battle["def_damage"] = battle["div"][div_id]["stats"]["def"][
                            "damage"
                        ]
                    else:
                        battle["def_damage"] = 0
                    if battle["inv_damage"] < 30000 or battle["def_damage"] < 30000:
                        picked_battles.append(battle)
        if len(picked_battles) > 0:
            picked_battles.sort(key=lambda battle: -battle["delay"])
            embed = discord.Embed(colour=discord.Colour(0xCE2C19))
            embed.set_author(name="SHs")
            embed.set_footer(
                text="Powered by https://erepublik.tools",
                icon_url="https://erepublik.tools/assets/img/icon76.png",
            )
            battle_text = ""
            damage_text = ""
            time_text = ""
            for battle in picked_battles:
                if len(battle_text) > 900:
                    embed.add_field(name="Battle", value=battle_text, inline=True)
                    embed.add_field(name="Damage", value=damage_text, inline=True)
                    embed.add_field(name="Time", value=time_text, inline=True)
                    battle_text = ""
                    damage_text = ""
                    time_text = ""
                if "started_since" in battle:
                    battle_text = "{}{}-{} [{}](https://www.erepublik.com/en/military/battlefield/{})\n".format(
                        battle_text,
                        self.utils.get_country_flag(battle["inv"]["id"]),
                        self.utils.get_country_flag(battle["def"]["id"]),
                        battle["region"]["name"],
                        battle["id"],
                    )
                    damage_text = "{}{:<6}-{:>6}\n".format(
                        damage_text, battle["inv_damage"], battle["def_damage"]
                    )
                    time_text = "{}+{}m{}s\n".format(
                        time_text,
                        battle["started_since"] // 60,
                        battle["started_since"] % 60,
                    )
                else:
                    battle_text = "{}{}-{} [{}](https://www.erepublik.com/en/military/battlefield/{})\n".format(
                        battle_text,
                        self.utils.get_country_flag(battle["inv"]["id"]),
                        self.utils.get_country_flag(battle["def"]["id"]),
                        battle["region"]["name"],
                        battle["id"],
                    )
                    damage_text = damage_text + ":airplane_departure:\n"
                    time_text = "{}-{}m{}s\n".format(
                        time_text, battle["delay"] // 60 % 60, battle["delay"] % 60
                    )
            embed.add_field(name="Battle", value=battle_text, inline=True)
            embed.add_field(name="Damage", value=damage_text, inline=True)
            embed.add_field(name="Time", value=time_text, inline=True)
            await ctx.send("", embed=embed)
        else:
            await ctx.send("No SH available at the moment")

    @commands.hybrid_command(aliases=["EPIC"])
    async def epic(self, ctx):
        """Returns the list of epic and fullscale battles"""
        r = requests.get("https://www.erepublik.com/en/military/campaignsJson/list")
        data = json.loads(r.text)
        battle_ids = [
            battle_id
            for battle_id in data["battles"]
            if any(
                [
                    True
                    for div in data["battles"][battle_id]["div"]
                    if data["battles"][battle_id]["div"][div]["epic"]
                    and not data["battles"][battle_id]["div"][div]["division_end"]
                ]
            )
        ]

        if len(battle_ids):
            battle_text = ""
            type_text = ""
            time_text = ""
            embed = discord.Embed(colour=discord.Colour(0xCE2C19))
            embed.set_author(name="Epics")
            embed.set_footer(
                text="Powered by https://erepublik.tools",
                icon_url="https://erepublik.tools/assets/img/icon76.png",
            )
            for battle_id in battle_ids:
                if (
                    len(embed) + len(battle_text) + len(type_text) + len(time_text)
                    > 6000
                ):
                    await ctx.send("", embed=embed)
                    embed = discord.Embed(colour=discord.Colour(0xCE2C19))
                    embed.set_author(name="Epics")
                    embed.set_footer(
                        text="Powered by https://erepublik.tools",
                        icon_url="https://erepublik.tools/assets/img/icon76.png",
                    )
                    embed.add_field(name="Battle", value=battle_text, inline=True)
                    embed.add_field(name="Type", value=type_text, inline=True)
                    embed.add_field(name="Time", value=time_text, inline=True)
                    battle_text = ""
                    type_text = ""
                    time_text = ""
                battle = data["battles"][battle_id]

                battle["started_since"] = data["time"] - battle["start"]
                divisions = [
                    (
                        battle["div"][div]["div"],
                        battle["div"][div]["epic"],
                        battle["div"][div]["epic_type"],
                    )
                    for div in [
                        div_id
                        for div_id in battle["div"]
                        if battle["div"][div_id]["epic"]
                    ]
                ]

                for division in divisions:
                    battle_text_new = "{}-{} [{}](https://www.erepublik.com/en/military/battlefield/{})\n".format(
                        self.utils.get_country_flag(battle["inv"]["id"]),
                        self.utils.get_country_flag(battle["def"]["id"]),
                        battle["region"]["name"],
                        battle["id"],
                    )
                    if len(battle_text) + len(battle_text_new) > 1024:
                        embed.add_field(name="Battle", value=battle_text, inline=True)
                        embed.add_field(name="Type", value=type_text, inline=True)
                        embed.add_field(name="Time", value=time_text, inline=True)
                        battle_text = battle_text_new
                        type_text = ""
                        time_text = ""
                    else:
                        battle_text += battle_text_new
                    if division[1] == 2:
                        if division[2] == 5:
                            type_text = "{}Most Contested-D{}\n".format(
                                type_text, division[0]
                            )
                        else:
                            type_text = "{}Epic-D{}\n".format(type_text, division[0])
                    else:
                        type_text = "{}Fullscale-D{}\n".format(type_text, division[0])
                    time_text = "{}+{}m{}s\n".format(
                        time_text,
                        battle["started_since"] // 60,
                        battle["started_since"] % 60,
                    )
            if len(embed) + len(battle_text) + len(type_text) + len(time_text) > 6000:
                await ctx.send("", embed=embed)
                embed = discord.Embed(colour=discord.Colour(0xCE2C19))
                embed.set_author(name="Epics")
                embed.set_footer(
                    text="Powered by https://erepublik.tools",
                    icon_url="https://erepublik.tools/assets/img/icon76.png",
                )
                embed.add_field(name="Battle", value=battle_text, inline=True)
                embed.add_field(name="Type", value=type_text, inline=True)
                embed.add_field(name="Time", value=time_text, inline=True)
                await ctx.send("", embed=embed)
            else:
                embed.add_field(name="Battle", value=battle_text, inline=True)
                embed.add_field(name="Type", value=type_text, inline=True)
                embed.add_field(name="Time", value=time_text, inline=True)
                await ctx.send("", embed=embed)
        else:
            await ctx.send("No epics or full-scale ongoing right now")

    @commands.hybrid_command(aliases=["CO"])
    async def co(self, ctx):
        """Returns the list of current combat orders"""
        r = requests.get("https://www.erepublik.com/en/military/campaignsJson/list")
        data = json.loads(r.text)
        battle_ids = [
            battle_id
            for battle_id in data["battles"]
            if any(
                [
                    True
                    for div in data["battles"][battle_id]["div"]
                    if data["battles"][battle_id]["div"][div]["co"]["inv"]
                    or data["battles"][battle_id]["div"][div]["co"]["def"]
                ]
            )
        ]

        if len(battle_ids):
            battle_text = ""
            currency_text = ""
            threshold_text = ""
            embed = discord.Embed(colour=discord.Colour(0xCE2C19))
            embed.set_author(name="Combat Orders")
            embed.set_footer(
                text="Powered by https://erepublik.tools",
                icon_url="https://erepublik.tools/assets/img/icon76.png",
            )
            for battle_id in battle_ids:
                if (
                    len(embed)
                    + len(battle_text)
                    + len(currency_text)
                    + len(threshold_text)
                    > 6000
                ):
                    await ctx.send("", embed=embed)
                    embed = discord.Embed(colour=discord.Colour(0xCE2C19))
                    embed.set_author(name="Combat orders")
                    embed.set_footer(
                        text="Powered by https://erepublik.tools",
                        icon_url="https://erepublik.tools/assets/img/icon76.png",
                    )
                    embed.add_field(name="Battle", value=battle_text, inline=True)
                    embed.add_field(
                        name="Reward per 1M (Budget)", value=currency_text, inline=True
                    )
                    embed.add_field(
                        name="Threshold (Current)", value=threshold_text, inline=True
                    )
                    battle_text = ""
                    currency_text = ""
                    threshold_text = ""

                battle = data["battles"][battle_id]

                divs_inv = [
                    (div_id)
                    for div_id in battle["div"]
                    if battle["div"][div_id]["co"]["inv"]
                ]

                co_inv = []
                ids_inv = []
                for div in divs_inv:
                    for co in battle["div"][div]["co"]["inv"]:
                        if co["co_id"] not in ids_inv:
                            ids_inv.append(co["co_id"])
                            co_item = co
                            co_item["div"] = battle["div"][div]["div"]
                            co_item["div_id"] = div
                            if battle["div"][div]["wall"]["for"] == battle["inv"]["id"]:
                                co_item["wall"] = battle["div"][div]["wall"]["dom"]
                            else:
                                co_item["wall"] = 100 - float(
                                    battle["div"][div]["wall"]["dom"]
                                )
                            co_inv.append(co_item)

                divs_def = [
                    (div_id)
                    for div_id in battle["div"]
                    if battle["div"][div_id]["co"]["def"]
                ]

                co_def = []
                ids_def = []
                for div in divs_def:
                    for co in battle["div"][div]["co"]["def"]:
                        if co["co_id"] not in ids_def:
                            ids_def.append(co["co_id"])
                            co_item = co
                            co_item["div"] = battle["div"][div]["div"]
                            co_item["div_id"] = div
                            if battle["div"][div]["wall"]["for"] == battle["def"]["id"]:
                                co_item["wall"] = battle["div"][div]["wall"]["dom"]
                            else:
                                co_item["wall"] = 100 - float(
                                    battle["div"][div]["wall"]["dom"]
                                )
                            co_def.append(co_item)

                for co in co_inv:
                    battle_text_new = "{} D{} [{}](https://www.erepublik.com/en/military/battlefield/{}/{})\n".format(
                        self.utils.get_country_flag(battle["inv"]["id"]),
                        co["div"],
                        battle["region"]["name"],
                        battle["id"],
                        co["div_id"],
                    )
                    if len(battle_text) + len(battle_text_new) > 1024:
                        embed.add_field(name="Battle", value=battle_text, inline=True)
                        embed.add_field(
                            name="Reward per 1M (Budget)",
                            value=currency_text,
                            inline=True,
                        )
                        embed.add_field(
                            name="Threshold (Current)",
                            value=threshold_text,
                            inline=True,
                        )
                        battle_text = battle_text_new
                        currency_text = ""
                        threshold_text = ""
                    else:
                        battle_text += battle_text_new
                    currency_text = "{}{} ({})\n".format(
                        currency_text, co["reward"], co["budget"]
                    )

                    threshold_text = "{}{}% ({:.2f}%)\n".format(
                        threshold_text, co["threshold"], co["wall"],
                    )

                for co in co_def:
                    battle_text_new = "{} D{} [{}](https://www.erepublik.com/en/military/battlefield/{}/{})\n".format(
                        self.utils.get_country_flag(battle["def"]["id"]),
                        co["div"],
                        battle["region"]["name"],
                        battle["id"],
                        co["div_id"],
                    )
                    if len(battle_text) + len(battle_text_new) > 1024:
                        embed.add_field(name="Battle", value=battle_text, inline=True)
                        embed.add_field(name="Reward", value=currency_text, inline=True)
                        embed.add_field(
                            name="Threshold (Current)",
                            value=threshold_text,
                            inline=True,
                        )
                        battle_text = battle_text_new
                        currency_text = ""
                        threshold_text = ""
                    else:
                        battle_text += battle_text_new
                    currency_text = "{}{} ({})\n".format(
                        currency_text, co["reward"], co["budget"]
                    )

                    threshold_text = "{}{}% ({:.2f}%)\n".format(
                        threshold_text, co["threshold"], co["wall"],
                    )
            if (
                len(embed) + len(battle_text) + len(currency_text) + len(threshold_text)
                > 6000
            ):
                await ctx.send("", embed=embed)
                embed = discord.Embed(colour=discord.Colour(0xCE2C19))
                embed.set_author(name="Combat Orders")
                embed.set_footer(
                    text="Powered by https://erepublik.tools",
                    icon_url="https://erepublik.tools/assets/img/icon76.png",
                )
                embed.add_field(name="Battle", value=battle_text, inline=True)
                embed.add_field(
                    name="Reward per 1M (Budget)", value=currency_text, inline=True
                )
                embed.add_field(
                    name="Threshold (Current)", value=threshold_text, inline=True
                )
                await ctx.send("", embed=embed)
            else:
                embed.add_field(name="Battle", value=battle_text, inline=True)
                embed.add_field(
                    name="Reward per 1M (Budget)", value=currency_text, inline=True
                )
                embed.add_field(
                    name="Threshold (Current)", value=threshold_text, inline=True
                )
                await ctx.send("", embed=embed)
        else:
            await ctx.send("No combat orders right now")


async def setup(bot):
    await bot.add_cog(Battle(bot))