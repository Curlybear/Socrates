import discord
from discord.ext import commands
import configparser
import logging
import requests
import json

import ereputils

logger = logging.getLogger('Socrates.User')

# Config reader
config = configparser.ConfigParser()
config.read('config.ini')

# API Key
apiKey = config['DEFAULT']['api_key']


class User:
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    async def find_user(self, ctx, in_value):
        user_text = ''
        user_id = ''
        user_name = ''
        if self.utils.is_number(in_value):
            user_id = str(int(in_value))
            try:
                user_name = (self.utils.get_user_id(user_id))[0][0]
            except Exception:
                user_name = ''
        else:
            user_data = self.utils.get_user(in_value)
            if len(user_data) == 1:
                user_id = str(int(user_data[0][1]))
                user_name = user_data[0][0]
            else:
                if 1 < len(user_data) <= 9:
                    i = 1
                    for citizen in user_data:
                        user_text += str(i) + ') **' + citizen[0] + '** - *' + str(int(citizen[1])) + '*\n'
                        i += 1
                    em = discord.Embed(title='Please enter the number of the targeted citizen',
                                       description=user_text,
                                       colour=0x3D9900)
                    await self.bot.send_message(ctx.message.channel, '', embed=em)
                    msg = await self.bot.wait_for_message(author=ctx.message.author)
                    if int(msg.content) >= i or int(msg.content) < 1:
                        await self.bot.say('Invalid choice')
                        return
                    user_id = str(int(user_data[int(msg.content) - 1][1]))
                    user_name = user_data[int(msg.content) - 1][0]
                else:
                    if len(user_data) > 9:
                        user_text += '***' + in_value + '*** yields too many results (*' + str(
                            len(user_data)) + '*).\nPlease specify a more precise username'
                    if len(user_data) == 0:
                        user_text += '***' + in_value + '*** doesn\'t match any known citizens.'

                    em = discord.Embed(title='Citizen information', description=user_text, colour=0x3D9900)
                    await self.bot.send_message(ctx.message.channel, '', embed=em)
                    return
        return user_id, user_name

    @commands.command(pass_context=True, aliases=['USER'])
    async def user(self, ctx, *, in_value):
        logger.info('!user ' + in_value + ' - User: ' + str(ctx.message.author))

        found_user = await self.find_user(ctx, in_value)

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/players/details/' + found_user[0])
        obj = json.loads(r.text)

        citizen = obj['players'][found_user[0]]

        embed = discord.Embed(colour=discord.Colour(0xf5a623))
        embed.set_thumbnail(
            url='https://erepublik.tools/avatar/citizen/' + str(citizen['citizen_id']) + '.jpg')
        embed.set_author(name=citizen['name'], url='https://www.erepublik.com/en/citizen/profile/' + str(citizen['citizen_id']),
                         icon_url='https://erepublik.tools/avatar/citizen/' + str(citizen['citizen_id']) + ".jpg")
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')

        embed.add_field(name='Status', value=('Alive' if citizen['general']['is_alive'] else 'Dead'), inline=True)
        embed.add_field(name='Date registered', value=citizen['general']['registered'], inline=True)
        embed.add_field(name='ID', value=str(citizen['citizen_id']), inline=True)
        embed.add_field(name='Level', value=str(citizen['general']['level']), inline=True)
        embed.add_field(name='Division', value=str(citizen['military']['division']), inline=True)
        embed.add_field(name='Citizenship', value=self.utils.get_country_flag(
            citizen['citizenship']['country_id']) + ' ' + citizen['citizenship']['country_name'], inline=True)
        if citizen['military_unit']['name']:
            embed.add_field(name='Military Unit', value='[' + citizen['military_unit']['name'] + '](https://www.erepublik.com/en/military/military-unit/' + str(citizen['military_unit']['id']) + ')', inline=True)
        if citizen['party']['name']:
            embed.add_field(name='Party', value='[' + citizen['party']['name'] + '](https://www.erepublik.com/en/party/' + str(citizen['party']['id']) + ')', inline=True)
        embed.add_field(name='Strength', value=str(citizen['military']['strength']), inline=True)
        embed.add_field(name='Perception', value=str(citizen['military']['perception']), inline=True)
        embed.add_field(name='Rank', value=str(citizen['military']['rank_name']).replace('*', '\*'), inline=True)
        embed.add_field(name='Aircraft rank', value=str(citizen['military']['rank_name_aircraft']).replace('*', '\*'), inline=True)
        if citizen['newspaper']['name']:
            embed.add_field(name='Newspaper', value='[' + citizen['newspaper']['name'] + '](https://www.erepublik.com/en/newspaper/' + str(citizen['newspaper']['id']) + ')', inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.group(pass_context=True, aliases=['HISTORY'])
    async def history(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid history command passed...')

    @history.command(pass_context=True, aliases=['CS'])
    async def cs(self, ctx, *, in_value: str):
        logger.info('!history cs ' + in_value + ' - User: ' + str(ctx.message.author))
        user_text = ['', '', '', '']

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/players/history/cs/' + found_user[0])
        obj = json.loads(r.text)
        user_text[0] = ''
        i = 0
        hists = obj['history'][found_user[0]]['cs']

        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x['added'])
            for hist in hists:
                user_text[i] += self.utils.get_country_flag(hist['country_id_from']) + ' ***' + hist[
                    'country_name_from'] + '*** to ' + self.utils.get_country_flag(
                    hist['country_id_to']) + ' ***' + hist['country_name_to'] + '*** on ' + hist['added'] + '\n'
                if len(user_text[i]) > 1800:
                    user_text[i] += '...'
                    i += 1
        else:
            user_text[0] = 'No history to display.'

        embed = discord.Embed(colour=discord.Colour(0xf5a623))
        embed.set_thumbnail(
            url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + '.jpg')
        embed.set_author(name=str(found_user[1]),
                         url='https://www.erepublik.com/en/citizen/profile/' + str(found_user[0]),
                         icon_url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + ".jpg")
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')

        i = 0
        while len(user_text[i]):
            embed.description = user_text[i]
            await self.bot.send_message(ctx.message.channel, '', embed=embed)
            i += 1

    @history.command(pass_context=True, aliases=['NAME'])
    async def name(self, ctx, *, in_value: str):
        logger.info('!history name ' + in_value + ' - User: ' + str(ctx.message.author))
        user_text = ['', '', '', '']

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/players/history/name/' + found_user[0])
        obj = json.loads(r.text)
        user_text[0] = ''
        i = 0
        hists = obj['history'][found_user[0]]['name']
        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x['added'])
            for hist in hists:
                user_text[i] += '***' + hist['name_from'] + '*** to ***' + hist['name_to'] + '*** on ' + hist[
                    'added'] + '\n'
                if len(user_text[i]) > 1800:
                    user_text[i] += '...'
                    i += 1
        else:
            user_text[0] = 'No history to display.'

        embed = discord.Embed(colour=discord.Colour(0xf5a623))
        embed.set_thumbnail(
            url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + '.jpg')
        embed.set_author(name=str(found_user[1]),
                         url='https://www.erepublik.com/en/citizen/profile/' + str(found_user[0]),
                         icon_url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + ".jpg")
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')

        i = 0
        while len(user_text[i]):
            embed.description=user_text[i]
            await self.bot.send_message(ctx.message.channel, '', embed=embed)
            i += 1

    @history.command(pass_context=True, aliases=['MU'])
    async def mu(self, ctx, *, in_value: str):
        logger.info('!history mu ' + in_value + ' - User: ' + str(ctx.message.author))
        user_text = ['', '', '', '']

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/players/history/mu/' + found_user[0])
        obj = json.loads(r.text)
        user_text[0] = ''
        i = 0
        hists = obj['history'][found_user[0]]['mu']
        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x['added'])
            for hist in hists:
                user_text[i] += 'From ' + ('[' + hist['mu_name_from'] + '](https://www.erepublik.com/en/military/military-unit/' + str(hist['mu_id_from']) + ')' if hist['mu_name_from'] is not None else '***None***')
                user_text[i] += ' to ' + ('[' + hist['mu_name_to'] + '](https://www.erepublik.com/en/military/military-unit/' + str(hist['mu_id_to']) + ')' if hist['mu_name_to'] is not None else '***None***')
                user_text[i] += ' (' + hist['added'] + ')\n'
                if len(user_text[i]) > 1800:
                    user_text[i] += '...'
                    i += 1
        else:
            user_text[0] = 'No history to display.'

        embed = discord.Embed(colour=discord.Colour(0xf5a623))
        embed.set_thumbnail(
            url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + '.jpg')
        embed.set_author(name=str(found_user[1]),
                         url='https://www.erepublik.com/en/citizen/profile/' + str(found_user[0]),
                         icon_url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + ".jpg")
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')

        i = 0
        while len(user_text[i]):
            embed.description=user_text[i]
            await self.bot.send_message(ctx.message.channel, '', embed=embed)
            i += 1

    @history.command(pass_context=True, aliases=['PARTY'])
    async def party(self, ctx, *, in_value: str):
        logger.info('!history party ' + in_value + ' - User: ' + str(ctx.message.author))
        user_text = ['', '', '', '']

        found_user = await self.find_user(ctx, in_value)
        if not found_user:
            return

        r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/players/history/party/' + found_user[0])
        obj = json.loads(r.text)
        user_text[0] = ''
        i = 0
        hists = obj['history'][found_user[0]]['party']
        if len(hists) > 0:
            hists = sorted(hists, key=lambda x: x['added'])
            for hist in hists:
                user_text[i] += 'From ' + ('[' + hist['party_name_from'] + '](https://www.erepublik.com/en/party/' + str(hist['party_id_from']) + ')' if hist['party_name_from'] is not None else '***None***')
                user_text[i] += ' to ' + ('[' + hist['party_name_to'] + '](https://www.erepublik.com/en/party/' + str(hist['party_id_to']) + ')' if hist['party_name_to'] is not None else '***None***')
                user_text[i] += ' (' + hist['added'] + ')\n'

                if len(user_text[i]) > 1800:
                    user_text[i] += '...'
                    i += 1
        else:
            user_text[0] = 'No history to display.'

        embed = discord.Embed(colour=discord.Colour(0xf5a623))
        embed.set_thumbnail(
            url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + '.jpg')
        embed.set_author(name=str(found_user[1]),
                         url='https://www.erepublik.com/en/citizen/profile/' + str(found_user[0]),
                         icon_url='https://erepublik.tools/avatar/citizen/' + str(found_user[0]) + ".jpg")
        embed.set_footer(text='Powered by https://www.erepublik-deutschland.de/en',
                         icon_url='https://www.erepublik-deutschland.de/assets/img/logo1-default_small.png')

        i = 0
        while len(user_text[i]):
            embed.description=user_text[i]
            await self.bot.send_message(ctx.message.channel, '', embed=embed)
            i += 1


def setup(bot):
    bot.add_cog(User(bot))
