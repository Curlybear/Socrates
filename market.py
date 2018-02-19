import discord
from discord.ext import commands
import configparser
import logging
import requests
import json

import ereputils

logger = logging.getLogger('Socrates.Country')

# Config reader
config = configparser.ConfigParser()
config.read('config.ini')

# API Key
apiKey = config['DEFAULT']['api_key']


class Market:
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.command(pass_context=True, aliases=['FOOD'])
    async def food(self, ctx, in_quality: str):
        logger.info('!food ' + in_quality + ' - User: ' + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/food/' + in_quality)
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best Q' + in_quality + ' food offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/1_' + in_quality + '.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['WEAPONS'])
    async def weapons(self, ctx, in_quality: str):
        logger.info('!weapons ' + in_quality + ' - User: ' + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/weapons/' + in_quality)
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best Q' + in_quality + ' weapons offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/2_' + in_quality + '.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['AIRCRAFT'])
    async def aircraft(self, ctx, in_quality: str = '1'):
        logger.info('!aircraft ' + in_quality + ' - User: ' + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/aircraft/' + in_quality)
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(
                    offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best Q' + in_quality + ' aircraft offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/23_' + in_quality + '.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['HOUSE'])
    async def house(self, ctx, in_quality: str):
        logger.info('!house ' + in_quality + ' - User: ' + str(ctx.message.author))
        if not self.utils.is_number(in_quality):
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/houses/' + in_quality)
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(
                    offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best Q' + in_quality + ' aircraft offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/4_' + in_quality + '.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['FRM'])
    async def frm(self, ctx):
        logger.info('!frm - User: ' + str(ctx.message.author))

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/frm/1')
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(
                    offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best frm offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/7_1.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['WRM'])
    async def wrm(self, ctx):
        logger.info('!wrm - User: ' + str(ctx.message.author))

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/wrm/1')
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(
                    offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best wrm offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/12_1.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['HRM'])
    async def hrm(self, ctx):
        logger.info('!hrm - User: ' + str(ctx.message.author))

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/hrm/1')
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(
                    offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best hrm offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/17_1.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['ARM'])
    async def arm(self, ctx):
        logger.info('!arm - User: ' + str(ctx.message.author))

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/market/bestoffers/arm/1')
        obj = json.loads(r.text)
        offers = obj['bestoffers']

        countries = ''
        prices = ''
        links = ''
        if not offers:
            await self.bot.send_message(ctx.message.channel, 'No matching offers')
        else:
            for i in range(10):
                flag = self.utils.get_country_flag(offers[i]['country_id'])
                countries += flag + ' ' + offers[i]['country_name'] + '\n'
                prices += ':dollar: ' + str(offers[i]['price']) + ' - :package: ' + str(offers[i]['amount']) + '\n'
                links += ':link: [Link to offer](https://www.erepublik.com/en/economy/marketplace/offer/' + str(
                    offers[i]['offer_id']) + ')' + '\n'

        embed = discord.Embed(colour=discord.Colour(0xce2c19))
        embed.set_author(name='Best hrm offers',
                         icon_url='https://static.erepublik.tools/assets/img/erepublik/industry/24_1.png')
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')
        embed.add_field(name="Country", value=countries, inline=True)
        embed.add_field(name="Price - Quantity", value=prices, inline=True)
        embed.add_field(name="Link", value=links, inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)


def setup(bot):
    bot.add_cog(Market(bot))
