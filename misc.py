import datetime
import traceback
import check

import discord
from discord.ext import commands
import logging

import ereputils

logger = logging.getLogger('Socrates.Misc')


class Misc:
    
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.command(pass_context=True, aliases=['PING'])
    async def ping(self, ctx):
        """Pings the bot"""
        logger.info('!ping - User: ' + str(ctx.message.author))
        em = discord.Embed(title='Pong', description='pong', colour=0x3D9900)
        await self.bot.send_message(ctx.message.channel, '', embed=em)

    @commands.command(pass_context=True, aliases=['HELP'])
    async def help(self, ctx):
        logger.info('!help - User: ' + str(ctx.message.author))
        em = discord.Embed(title='Help', description='Available commands', colour=0x0053A9)
        em.add_field(name="!alliances",
                     value="Return a visual representation of the alliances", inline=False)
        em.add_field(name="!battle (info|co) [battleid]", value="Return the information regarding a specified battle",
                     inline=False)
        em.add_field(name="!cinfo [country name]", value="Returns a list of information for the specified country",
                     inline=False)
        em.add_field(name="!convert [erepDay|date]",
                     value="Return the conversion of the provided erepDay or date (dd/mm/yyyy)", inline=False)
        em.add_field(name="!help",
                     value="Return this help message", inline=False)
        em.add_field(name="!history (cs|name|mu|party) [username|userid]",
                     value="Return a specific history of information for a specified user", inline=False)
        em.add_field(name="!invite",
                     value="Return the link to invite Socrates to your own server", inline=False)
        em.add_field(name="!(food|weapons|aircrafts|houses|tickets|frm|wrm|arm|hrm) [quality]", value="Returns a list of the best offers for the given product")
        em.add_field(name="!jobs", value="Returns the top jobs overall",
                     inline=False)
        em.add_field(name="!mpp [country name]", value="Returns a list of mpps for the specified country", inline=False)
        em.add_field(name="!user [username|userid]", value="Return the information regarding a specified user",
                     inline=False)
        em.add_field(name="!wiki [entry name]",
                     value="Return the information relative to the queried entry", inline=False)
        em.add_field(name="!wikicats",
                     value="Return the categories available in the wiki", inline=False)
        em.add_field(name="!wikilist [category]",
                     value="Return the list of entries belonging to a given category", inline=False)
        em.set_author(name="Curlybear#1962", url='https://curlybear.eu',
                      icon_url='https://erpk-static-avatars.s3.amazonaws.com/avatars/Citizens/2011/07/12/0a83af20636fe1ac4d01c6d132572943.png?8e8837b38eeff670f9301b95d31a47a2')
        em.set_thumbnail(url='http://www.dipsacademy.com/images/socrates.png')
        em.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                      icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        await self.bot.send_message(ctx.message.channel, '', embed=em)

    @commands.command(pass_context=True, aliases=['CONVERT'])
    async def convert(self, ctx, in_value: str):
        logger.info('!convert ' + in_value + ' - User: ' + str(ctx.message.author))

        start_date = datetime.datetime(day=21, month=11, year=2007)
        try:
            if self.utils.is_number(in_value):
                delta = datetime.timedelta(days=int(in_value) - 1)
                final_date = start_date + delta
                em = discord.Embed(title='Conversion', description='Date : ' + final_date.strftime('%d/%m/%Y'),
                                   colour=0x0053A9)
                await self.bot.send_message(ctx.message.channel, '', embed=em)
            else:
                in_date = datetime.datetime.strptime(in_value, '%d/%m/%Y')
                erep_day = in_date - start_date + datetime.timedelta(days=1)
                em = discord.Embed(title='Conversion', description='eRepublik day : ' + str(erep_day.days),
                                   colour=0x0053A9)
                await self.bot.send_message(ctx.message.channel, '', embed=em)
        except:
            traceback.print_exc()
            logger.info('   Invalid input')
            await self.bot.say('Invalid input')

    @commands.command(pass_context=True, aliases=['INVITE'])
    async def invite(self, ctx):
        logger.info('!' + str(ctx.invoked_subcommand) + ' - User: ' + str(ctx.message.author))
        await self.bot.send_message(ctx.message.channel, 'To invite me to your own server click the following link: <https://discordapp.com/oauth2/authorize?client_id=304725683995934723&scope=bot&permissions=0>')

    @commands.command(pass_context=True, aliases=['ANNOUNCEMENT'])
    @check.is_authorized_staff()
    async def announcement(self, ctx, *, message: str):
        logger.info('!announcement ' + message + ' - User: ' + str(ctx.message.author))
        for server in self.bot.servers:
            try:
                await self.bot.send_message(server, message + '\n\nSent by: *' + str(ctx.message.author) + '*')
                logger.info('   Sent to: ' + str(server))
            except:
                logger.info('   Not sent to: ' + str(server))
                pass


def setup(bot):
    bot.add_cog(Misc(bot))
