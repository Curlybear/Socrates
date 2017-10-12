import discord
from discord.ext import commands
import configparser
import logging
import requests
import json
from PythonGists import PythonGists
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
            r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/countries/details/' + str(uid))
            obj = json.loads(r.text)
            mpps = obj['countries'][str(uid)]['military']['mpps']
            if not mpps:
                mpp_text += '**No MPPs**'
            else:
                mpps.sort(key = lambda x: x['expires'][0:10])
                for mpp in mpps:
                    mpp_text += self.utils.get_country_flag(mpp['country_id']) + ' **' + self.utils.get_country_name(
                        mpp['country_id']) + '** - ' + mpp['expires'][0:10] + '\n'
            em = discord.Embed(title='MPPs of ' + self.utils.get_country_flag(uid) + ' ' + country + '',
                               description=mpp_text, colour=0x0053A9)
            await self.bot.send_message(ctx.message.channel, '', embed=em)
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

        link = PythonGists.Gist(description='eRepublik MPPs', content=mpp_text, name='mpps' + datetime.datetime.now().strftime("%d-%m-%Y") + '.csv')
        em = discord.Embed(title='All MPPs',
                           description=link, colour=0x0042B9)
        await self.bot.send_message(ctx.message.channel, '', embed=em)

    @commands.command(pass_context=True, aliases=['CINFO'])
    async def cinfo(self, ctx, *, in_country: str):
        logger.info('!cinfo ' + in_country + ' - User: ' + str(ctx.message.author))
        try:
            uid = self.utils.get_country_id(in_country)
            country = self.utils.get_country_name(uid)
            r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/countries/details/' + str(uid))
            obj = json.loads(r.text)
            pop_text = '**Population:** *' + str(obj['countries'][str(uid)]['population']['total']) + '* citizens\n'
            eco_text = '**Economy:** \n**CC:** *' + str(
                obj['countries'][str(uid)]['economy']['cc']) + '* \n**Gold:** *' + str(
                obj['countries'][str(uid)]['economy']['gold']) + '* \n**Average salary:** *' + str(
                obj['countries'][str(uid)]['economy']['salary_average']) + '* \n'
            admin_text = '**Administration:** \n'
            if obj['countries'][str(uid)]['administration']['dictator']['id']:
                admin_text += '**Dictator:** *' + obj['countries'][str(uid)]['administration']['dictator'][
                    'name'] + '* - ' + 'https://www.erepublik.com/en/citizen/profile/' + str(
                    obj['countries'][str(uid)]['administration']['dictator']['id']) + '\n'
            if obj['countries'][str(uid)]['administration']['president']['id']:
                admin_text += '**President:** *' + obj['countries'][str(uid)]['administration']['president'][
                    'name'] + '* - ' + 'https://www.erepublik.com/en/citizen/profile/' + str(
                    obj['countries'][str(uid)]['administration']['president']['id']) + '\n'
            for minister in obj['countries'][str(uid)]['administration']['minister']:
                admin_text += '**' + minister + ':** *' + \
                             obj['countries'][str(uid)]['administration']['minister'][minister][
                                 'name'] + '* - ' + 'https://www.erepublik.com/en/citizen/profile/' + str(
                    obj['countries'][str(uid)]['administration']['minister'][minister]['id']) + '\n'
            em = discord.Embed(title='Information about ' + self.utils.get_country_flag(uid) + ' ' + country + ':',
                               description=admin_text + pop_text + eco_text, colour=0x0053A9)
            await self.bot.send_message(ctx.message.channel, '', embed=em)
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
