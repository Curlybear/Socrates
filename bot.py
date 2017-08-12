import discord
from discord.ext import commands
import configparser
import logging


# Config reader
config = configparser.ConfigParser()
config.read('config.ini')

# Set up logging
logger = logging.getLogger('Socrates')
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('bot.log')
handler.setLevel(logging.INFO)
handlerError = logging.FileHandler('botError.log')
handlerError.setLevel(logging.ERROR)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# API Key
apiKey = config['DEFAULT']['api_key']

# Instantiate bot
description = 'Available commands \n !mpp [country name] - Returns a list of mpps for the specified country \n !jobs [number|country name]- Returns the top jobs overall or for a specific country \n !cinfo [country name] - Returns a list of information for the specified country \n !user [username|userid] - Return the information regarding a specified user \n !history (cs|name|mu|party) [username|userid] - Return a specific history of information for a specified user \n !battle (info|co) [battleid] - Return the information regarding a specified battle\n\nMore information at https://curlybear.eu/socrates \nPowered by erepublik-deutschland.de'
bot = commands.Bot(command_prefix='!', description=description)
bot.remove_command("help")

# this specifies what extensions to load when the bot starts up
startup_extensions = ["misc", "country", "user", "battle"]


@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        logger.error("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    logger.info("{} loaded.".format(extension_name))


@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    logger.info("{} unloaded.".format(extension_name))

# Events


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    logger.info('Bot started as ' + bot.user.name)
    for server in bot.servers:
        logger.info('   ' + server.name)
    await bot.change_presence(game=discord.Game(name='eRepublik'))


@bot.event
async def on_server_join(server):
    logger.info('Bot joined: ' + server.name)


@bot.event
async def on_server_remove(server):
    logger.info('Bot left: ' + server.name)


@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await bot.add_reaction(message, '❤')
        logger.info('Mentionned by ' + message.author.name)
    await bot.process_commands(message)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            logger.warn('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config['DEFAULT']['bot_token'])
