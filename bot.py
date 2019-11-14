import configparser
import logging
from logging.handlers import SysLogHandler

import discord
from discord.ext import commands

import check

# Config reader
config = configparser.ConfigParser()
config.read("config.ini")

# Set up logging
logger = logging.getLogger("Socrates")
logger.setLevel(logging.INFO)

# create logging formats
formatter_file = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"
)

formatter_syslog = logging.Formatter(
    "[SOCRATES] %(levelname)s - %(name)s - %(funcName)s - %(message)s"
)

# create a file handler
handler = logging.FileHandler("bot.log")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter_file)

# create a syslog handler
syslog_handler = SysLogHandler(address="/dev/log")
syslog_handler.setLevel(logging.INFO)
syslog_handler.setFormatter(formatter_syslog)

# add the handlers to the logger
logger.addHandler(handler)
logger.addHandler(syslog_handler)

# API Key
apiKey = config["DEFAULT"]["api_key"]

# Instantiate bot
description = ""
bot = commands.Bot(command_prefix="!", description=description)
bot.remove_command("help")

# this specifies what extensions to load when the bot starts up
startup_extensions = ["misc", "country", "user", "battle", "wiki", "market"]


@bot.command()
@check.is_owner()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        logger.error("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    logger.info("{} loaded.".format(extension_name))


@bot.command()
@check.is_owner()
async def unload(extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    logger.info("{} unloaded.".format(extension_name))


# Events


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    logger.info("Bot started as " + bot.user.name)
    for guild in bot.guilds:
        logger.debug("   " + guild.name)
    await bot.change_presence(activity=discord.Game(name="eRepublik"))


@bot.event
async def on_guild_join(guild):
    logger.info("Bot joined: " + guild.name)


@bot.event
async def on_server_remove(server):
    logger.info("Bot left: " + server.name)


@bot.event
async def on_message(message):
    logger.debug(message.content)
    if bot.user in message.mentions:
        await message.add_reaction("❤")
        logger.info("Mentioned by " + message.author.name)
    await bot.process_commands(message)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            logger.warning("Failed to load extension {}\n{}".format(extension, exc))
    bot.run(config["DEFAULT"]["bot_token"])
