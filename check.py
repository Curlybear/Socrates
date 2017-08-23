from discord.ext import commands
import configparser

# Config reader
config = configparser.ConfigParser()
config.read('config.ini')


def is_owner_check(message):
    return message.author.id == config['DEFAULT']['owner_id']


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))
