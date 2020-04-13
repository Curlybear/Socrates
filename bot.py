import configparser
import logging
import traceback
from datetime import datetime
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

# create a file error handler
handlerError = logging.FileHandler("botError.log")
handlerError.setLevel(logging.WARNING)
handlerError.setFormatter(formatter_file)

# create a syslog handler
syslog_handler = SysLogHandler(address="/dev/log")
syslog_handler.setLevel(logging.INFO)
syslog_handler.setFormatter(formatter_syslog)

# add the handlers to the logger
logger.addHandler(handler)
logger.addHandler(handlerError)
logger.addHandler(syslog_handler)

# API Key
apiKey = config["DEFAULT"]["api_key"]

# Instantiate bot
description = ""
help_attrs = dict(hidden=True)
bot = commands.Bot(
    command_prefix="!",
    description=description,
    owner_id=int(config["DEFAULT"]["owner_id"]),
    help_attrs=help_attrs,
)
bot.uptimeStart = datetime.now()

# this specifies what extensions to load when the bot starts up
startup_extensions = ["country", "user", "battle", "market", "meta"]


@bot.command(hidden=True)
@check.is_owner()
async def load(ctx, extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        logger.error("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    logger.info("{} loaded.".format(extension_name))


@bot.command(hidden=True)
@check.is_owner()
async def unload(ctx, extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    logger.info("{} unloaded.".format(extension_name))


@bot.command(hidden=True)
@check.is_owner()
async def presence(ctx, *, presence_text: str):
    await bot.change_presence(activity=discord.Game(name=presence_text))


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


@bot.event
async def on_command(ctx):
    logger.info(f"{ctx.message.content} - User: {ctx.message.author}")
    return


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send("This command cannot be used in private messages.")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send("Sorry. This command is disabled and cannot be used.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            str(error) + "\n`!help " + ctx.invoked_with + "` for more infomation"
        )
    elif isinstance(error, commands.CommandInvokeError):
        original = error.original
        if not isinstance(original, discord.HTTPException):
            logger.warning(f"**Error in {ctx.invoked_with}**:{str(original)}")
            logger.warning("".join(traceback.format_tb(original.__traceback__)))
            logger.warning(ctx.__dict__)
            owner = bot.get_user(bot.owner_id)
            await owner.send(
                f"**Error original in {ctx.invoked_with}**:\n{str(original)}"
            )
    elif isinstance(
        error, (commands.ArgumentParsingError, commands.errors.CommandNotFound)
    ):
        pass
    else:
        logger.warning(f"**Error in {ctx.invoked_with}**:{str(error)}")
        logger.warning("".join(traceback.format_tb(error.__traceback__)))
        logger.warning(ctx.__dict__)
        owner = bot.get_user(bot.owner_id)
        await owner.send(f"**Error in {ctx.invoked_with}**:\n{str(error)}")


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            logger.warning("Failed to load extension {}\n{}".format(extension, exc))
    bot.run(config["DEFAULT"]["bot_token"])
