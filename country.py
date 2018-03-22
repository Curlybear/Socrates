import discord
from discord.ext import commands
import configparser
import logging
import requests
import json
import datetime

import ereputils

logger = logging.getLogger('Socrates.Country')

# Config reader
config = configparser.ConfigParser()
config.read('config.ini')

# API Key
apiKey = config['DEFAULT']['api_key']


class Country:
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.command(pass_context=True, aliases=['MPP'])
    async def mpp(self, ctx, *, in_country: str):
        logger.info('!mpp ' + in_country + ' - User: ' + str(ctx.message.author))
        try:
            uid = self.utils.get_country_id(in_country)
            country = self.utils.get_country_name(uid)
            mpp_text = ''
            expiration_text = ''
            r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/countries/details/' + str(uid))
            obj = json.loads(r.text)
            mpps = obj['countries'][str(uid)]['military']['mpps']
            if not mpps:
                mpp_text += '**No MPPs**'
                expiration_text += '**No MPPs**'
            else:
                mpps.sort(key = lambda x: x['expires'][0:10])
                for mpp in mpps:
                    mpp_text += self.utils.get_country_flag(mpp['country_id']) + ' **' + self.utils.get_country_name(
                        mpp['country_id']) + '**' + '\n'

                    expiration_text += ':small_blue_diamond: ' + mpp['expires'][0:10] + '\n'

            embed = discord.Embed(colour=discord.Colour(0xce2c19))
            embed.set_author(name=country + " Mutual Protection Pacts", icon_url='https://static.erepublik.tools/assets/img/erepublik/country/' + str(uid) + '.gif')
            embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                             icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')

            embed.add_field(name="Country", value=mpp_text, inline=True)
            embed.add_field(name="Expiration date", value=expiration_text, inline=True)
            await self.bot.send_message(ctx.message.channel, '', embed=embed)
        except:
            logger.info('\tCountry ***' + in_country + '*** not recognized')
            await self.bot.say('Country ***' + in_country + '*** not recognized')

    @commands.command(pass_context=True, aliases=['MPPSRAW'])
    async def mppsraw(self, ctx):
        logger.info('!mppsraw - User: ' + str(ctx.message.author))
        mpp_text = ''
        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/countries/details/all')
        obj = json.loads(r.text)
        for country in obj['countries']:
            mpps = obj['countries'][country]['military']['mpps']
            if mpps:
                mpps.sort(key=lambda x: x['expires'][0:10])
                for mpp in mpps:
                    mpp_text += self.utils.get_country_name(country) + ';' + self.utils.get_country_name(
                        mpp['country_id']) + ';' + mpp['expires'][0:10] + '\n'

        with open(config['PASTE']['paste_path'] + 'mpps' + datetime.datetime.now().strftime("%d-%m-%Y") + '.csv', 'w') as f:
            f.write(mpp_text)
        em = discord.Embed(title='All MPPs',
                           description=config['PASTE']['paste_url'] + 'mpps' + datetime.datetime.now().strftime("%d-%m-%Y") + '.csv', colour=0x0042B9)
        await self.bot.send_message(ctx.message.channel, '', embed=em)

    @commands.command(pass_context=True, aliases=['CINFO'])
    async def cinfo(self, ctx, *, in_country: str):
        logger.info('!cinfo ' + in_country + ' - User: ' + str(ctx.message.author))
        try:
            uid = self.utils.get_country_id(in_country)
            country = self.utils.get_country_name(uid)
            r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/countries/details/' + str(uid))
            obj = json.loads(r.text)

            embed = discord.Embed(colour=discord.Colour(0xce2c19))
            embed.set_author(name=country + " Information", icon_url='https://static.erepublik.tools/assets/img/erepublik/country/' + str(uid) + '.gif')
            embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                             icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')

            embed.add_field(name='Administration', value='--------------------------------------', inline=False)
            if obj['countries'][str(uid)]['administration']['dictator']['id']:
                embed.add_field(name='Dictator', value='[' + obj['countries'][str(uid)]['administration']['dictator']['name'] + '](https://www.erepublik.com/en/citizen/profile/' + str(obj['countries'][str(uid)]['administration']['dictator']['id']) + ')', inline=True)
            if obj['countries'][str(uid)]['administration']['president']['id']:
                embed.add_field(name='President', value='[' + obj['countries'][str(uid)]['administration']['president']['name'] + '](https://www.erepublik.com/en/citizen/profile/' + str(obj['countries'][str(uid)]['administration']['president']['id']) + ')', inline=True)
            for minister in obj['countries'][str(uid)]['administration']['minister']:
                embed.add_field(name=minister, value='[' + obj['countries'][str(uid)]['administration']['minister'][minister]['name'] + '](https://www.erepublik.com/en/citizen/profile/' + str(obj['countries'][str(uid)]['administration']['minister'][minister]['id']) + ')', inline=True)
            embed.add_field(name='Finance', value='--------------------------------------', inline=False)
            embed.add_field(name='CC', value=str(obj['countries'][str(uid)]['economy']['cc']), inline=True)
            embed.add_field(name='Gold', value=str(obj['countries'][str(uid)]['economy']['gold']), inline=True)
            embed.add_field(name='Average salary', value=str(obj['countries'][str(uid)]['economy']['salary_average']) + ' CC', inline=True)
            embed.add_field(name='Population', value=str(obj['countries'][str(uid)]['population']['total']) + ' citizens', inline=True)

            await self.bot.send_message(ctx.message.channel, '', embed=embed)
        except:
            logger.info('\tCountry ***' + in_country + '*** not recognized')
            await self.bot.say('Country ***' + in_country + '*** not recognized')

    @commands.command(pass_context=True)
    async def jobs(self, ctx, in_value='3'):
        # logger.info('!jobs ' + in_value + ' - User: ' + str(ctx.message.author))
        # jobtext = ''

        # if is_number(in_value):
        #     r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/jobmarket/bestoffers')
        #     obj = json.loads(r.text)
        #     in_value = int(in_value)
        #     if in_value > 5:
        #         in_value = 5
        #     for i in range(0, in_value):
        #         jobtext += self.utils.get_country_flag(obj['bestoffers'][i]['country_id']) + ' **' + obj['bestoffers'][i]['country_name'] + '** *' + obj['bestoffers'][i]['citizen_name'] + '*\n| Before work tax: ' + str(obj['bestoffers'][i]['salary'])+ '\n| After work tax: ' + str(obj['bestoffers'][i]['netto']) + '\n'
        #     em = discord.Embed(title='Best job offers:', description=jobtext, colour=0x0053A9)
        #     await self.bot.send_message(ctx.message.channel, '', embed=em)
        # if type(in_value) is str:
        #     try:
        #         nbrOffers = 3
        #         uid = self.utils.get_country_id(in_value)
        #         r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/jobmarket/countryoffers/' + str(uid))
        #         obj = json.loads(r.text)
        #         if len(obj['countryoffers']) == 0:
        #             jobtext += '**No offers available**'
        #         else:
        #             if len(obj['countryoffers'][str(uid)]) < 3:
        #                 nbrOffers = len(obj['countryoffers'][str(uid)])
        #             for i in range(0, nbrOffers):
        #                 jobtext += self.utils.get_country_flag(uid) +' **' + obj['countryoffers'][str(uid)][i]['citizen_name'] + '**\n| Before work tax: ' + str(obj['countryoffers'][str(uid)][i]['salary'])+ '\n| After work tax: ' + str(obj['countryoffers'][str(uid)][i]['netto']) + '\n'
        #         em = discord.Embed(title='Best job offers in ' + self.utils.get_country_flag(uid) + ' '+ in_value + ':', description=jobtext, colour=0x0053A9)
        #         await self.bot.send_message(ctx.message.channel, '', embed=em)
        #     except:
        #         logger.info('\tCountry ***' + in_value + '*** not recognized')
        #         await self.bot.say('Country ***' + in_value + '*** not recognized')
        await self.bot.say(
            'Broken at the moment. Visit https://erepublik.tools/marketplace/jobs/0/offers for updated informations on the available jobs.')


def setup(bot):
    bot.add_cog(Country(bot))
