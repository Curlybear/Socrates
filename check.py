from discord.ext import commands
import configparser
import json

# Config reader
config = configparser.ConfigParser()
config.read("config.ini")


def is_owner_check(message):
    return message.author.id == int(config["DEFAULT"]["owner_id"])


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


def is_authorized_staff_check(message):
    return message.author.id in json.loads(config.get("DEFAULT", "authorized_staff"))


def is_authorized_staff():
    return commands.check(lambda ctx: is_authorized_staff_check(ctx.message))
