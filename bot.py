import discord
from discord.ext import commands
import random
import requests
import json
import sqlite3
import datetime
import configparser
import logging
import sys
import traceback

#Config reader
config = configparser.ConfigParser()
config.read('config.ini')

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('bot.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

#DB Connection setup
conn = sqlite3.connect(config['DEFAULT']['db_name'])
c = conn.cursor()

#API Key
apiKey= config['DEFAULT']['api_key']

#Discord.py bot setup
description = 'Available commands \n !mpp [country name] - Returns a list of mpps for the specified country \n !jobs [number|country name]- Returns the top jobs overall or for a specific country \n !cinfo [country name] - Returns a list of information for the specified country \n !user [username|userid] - Return the information regarding a specified user \n !history (cs|name|mu|party) [username|userid] - Return a specific history of information for a specified user \n !battle (info|co) [battleid] - Return the information regarding a specified battle\n\nMore information at https://curlybear.eu/socrates \nPowered by erepublik-deutschland.de'

bot = commands.Bot(command_prefix='!', description=description)

bot.remove_command("help")

#Helper functions
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getCountryId(country_name):
    c.execute("SELECT id FROM countries WHERE name LIKE ?", ['%'+country_name+'%'])
    data = c.fetchone()
    return int(data[0])

def getCountryName(country_id):
    c.execute("SELECT name FROM countries WHERE id == ?", [country_id])
    data = c.fetchone()
    return data[0]

def getCountryFlag(country_id):
    c.execute("SELECT flag FROM countries WHERE id == ?", [country_id])
    data = c.fetchone()
    return data[0]

def getUser(username):
    c.execute("SELECT * FROM users WHERE username LIKE ?", [username+'%'])
    data = c.fetchall()
    return data

def getUserId(id):
    c.execute("SELECT * FROM users WHERE id = ?", [id])
    data = c.fetchall()
    return data

#Events
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

#Commands
@bot.command(pass_context=True)
async def help(ctx):
    logger.info('!help - User: ' + str(ctx.message.author))
    em = discord.Embed(title='Help', description='Available commands', colour=0x0053A9)
    em.add_field(name="!mpp [country name]", value="Returns a list of mpps for the specified country", inline=False)
    em.add_field(name="!jobs [number|country name]", value="Returns the top jobs overall or for a specific country", inline=False)
    em.add_field(name="!cinfo [country name]", value="Returns a list of information for the specified country", inline=False)
    em.add_field(name="!user [username|userid]", value="Return the information regarding a specified user", inline=False)
    em.add_field(name="!battle (info|co) [battleid]", value="Return the information regarding a specified battle", inline=False)
    em.add_field(name="!history (cs|name|mu|party) [username|userid]", value="Return a specific history of information for a specified user", inline=False)
    em.add_field(name="!convert [erepDay|date]", value="Return the conversion of the provided erepDay or date (dd/mm/yyyy)", inline=False)
    em.set_author(name="Curlybear#1962", url='https://curlybear.eu', icon_url='https://erpk-static-avatars.s3.amazonaws.com/avatars/Citizens/2011/07/12/0a83af20636fe1ac4d01c6d132572943.png?8e8837b38eeff670f9301b95d31a47a2')
    em.set_thumbnail(url='http://www.dipsacademy.com/images/socrates.png')
    em.set_footer(text='Powered by http://api.erepublik-deutschland.de/')
    await bot.send_message(ctx.message.channel, '', embed=em)
    
@bot.command(pass_context=True)
async def mpp(ctx, inCountry : str):
    logger.info('!mpp ' + inCountry + ' - User: ' + str(ctx.message.author))
    try:
        uid = getCountryId(inCountry)
        country = getCountryName(uid)
        mpptext = ''
        r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/countries/details/' + str(uid))
        obj = json.loads(r.text)
        mpps = obj['countries'][str(uid)]['military']['mpps']
        if not mpps:
           mpptext += '**No MPPs**'
        else:
           for mpp in mpps: 
               mpptext += getCountryFlag(mpp['country_id']) + ' **' + getCountryName(mpp['country_id']) + '** - ' + mpp['expires'][0:10] + '\n'
        em = discord.Embed(title='MPPs of ' + getCountryFlag(uid) + ' ' +  country + '', description=mpptext, colour=0x0053A9)
        await bot.send_message(ctx.message.channel, '', embed=em)
    except:
        logger.info('\tCountry ***' + inCountry + '*** not recognized')
        await bot.say('Country ***' + inCountry + '*** not recognized')

@bot.command(pass_context=True)
async def cinfo(ctx, inCountry : str):
    logger.info('!cinfo ' + inCountry + ' - User: ' + str(ctx.message.author))
    try:
        uid = getCountryId(inCountry)
        country = getCountryName(uid)
        r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/countries/details/' + str(uid))
        obj = json.loads(r.text)
        poptext = '**Population:** *' + str(obj['countries'][str(uid)]['population']['total']) + '* citizens\n'
        ecotext = '**Economy:** \n**CC:** *' +  str(obj['countries'][str(uid)]['economy']['cc']) + '* \n**Gold:** *' + str(obj['countries'][str(uid)]['economy']['gold']) + '* \n**Average salary:** *' + str(obj['countries'][str(uid)]['economy']['salary_average']) + '* \n'
        admintext = '**Administration:** \n'
        if obj['countries'][str(uid)]['administration']['dictator']['id']:
            admintext += '**Dictator:** *' +obj['countries'][str(uid)]['administration']['dictator']['name'] + '* - ' + 'https://www.erepublik.com/en/citizen/profile/' + str(obj['countries'][str(uid)]['administration']['dictator']['id']) + '\n'
        if obj['countries'][str(uid)]['administration']['president']['id']:
            admintext += '**President:** *' +obj['countries'][str(uid)]['administration']['president']['name'] + '* - ' + 'https://www.erepublik.com/en/citizen/profile/' + str(obj['countries'][str(uid)]['administration']['president']['id']) + '\n'
        for minister in obj['countries'][str(uid)]['administration']['minister']:
            admintext += '**' + minister + ':** *' +obj['countries'][str(uid)]['administration']['minister'][minister]['name'] + '* - ' + 'https://www.erepublik.com/en/citizen/profile/' + str(obj['countries'][str(uid)]['administration']['minister'][minister]['id']) + '\n'
        em = discord.Embed(title='Information about '+ getCountryFlag(uid) + ' ' + country + ':', description=admintext + poptext + ecotext, colour=0x0053A9)
        await bot.send_message(ctx.message.channel, '', embed=em)
    except:
        logger.info('\tCountry ***' + inCountry + '*** not recognized')
        await bot.say('Country ***' + inCountry + '*** not recognized')

@bot.command(pass_context=True)
async def jobs(ctx, inValue='3'):
    # logger.info('!jobs ' + inValue + ' - User: ' + str(ctx.message.author))
    # jobtext = ''

    # if is_number(inValue):
    #     r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/jobmarket/bestoffers')
    #     obj = json.loads(r.text)
    #     inValue = int(inValue)
    #     if inValue > 5:
    #         inValue = 5
    #     for i in range(0, inValue):
    #         jobtext += getCountryFlag(obj['bestoffers'][i]['country_id']) + ' **' + obj['bestoffers'][i]['country_name'] + '** *' + obj['bestoffers'][i]['citizen_name'] + '*\n| Before work tax: ' + str(obj['bestoffers'][i]['salary'])+ '\n| After work tax: ' + str(obj['bestoffers'][i]['netto']) + '\n'
    #     em = discord.Embed(title='Best job offers:', description=jobtext, colour=0x0053A9)
    #     await bot.send_message(ctx.message.channel, '', embed=em)
    # if type(inValue) is str:
    #     try:
    #         nbrOffers = 3
    #         uid = getCountryId(inValue)
    #         r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/jobmarket/countryoffers/' + str(uid))
    #         obj = json.loads(r.text)
    #         if len(obj['countryoffers']) == 0:
    #             jobtext += '**No offers available**'
    #         else:
    #             if len(obj['countryoffers'][str(uid)]) < 3:
    #                 nbrOffers = len(obj['countryoffers'][str(uid)])
    #             for i in range(0, nbrOffers):
    #                 jobtext += getCountryFlag(uid) +' **' + obj['countryoffers'][str(uid)][i]['citizen_name'] + '**\n| Before work tax: ' + str(obj['countryoffers'][str(uid)][i]['salary'])+ '\n| After work tax: ' + str(obj['countryoffers'][str(uid)][i]['netto']) + '\n'
    #         em = discord.Embed(title='Best job offers in ' + getCountryFlag(uid) + ' '+ inValue + ':', description=jobtext, colour=0x0053A9)
    #         await bot.send_message(ctx.message.channel, '', embed=em)
    #     except:
    #         logger.info('\tCountry ***' + inValue + '*** not recognized')
    #         await bot.say('Country ***' + inValue + '*** not recognized')
    await bot.say('Broken at the moment. Visit https://erepublik.tools/marketplace/jobs/0/offers for updated informations on the available jobs.')

@bot.command(pass_context=True)
async def user(ctx, inValue):
    logger.info('!user ' + inValue + ' - User: ' + str(ctx.message.author))
    usertext = ''
    userId = ''
    if is_number(inValue):
        userId = str(int(inValue))
    else:
        userdata = getUser(inValue)
        if len(userdata) == 1:
            userId = str(int(userdata[0][1]))
        else:
            if len(userdata) > 1 and len(userdata) <= 5:
                #Display all results then await choice
                i = 1
                for citizen in userdata:
                    usertext += str(i) + ') **' + citizen[0] + '** - *' + str(int(citizen[1])) + '*\n'
                    i += 1
                em = discord.Embed(title='Please enter the number of the targeted citizen', description=usertext, colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                msg = await bot.wait_for_message(author=ctx.message.author)
                if int(msg.content) >= i or int(msg.content) < 1:
                    await bot.say('Invalid choice')
                    return
                userId = str(int(userdata[int(msg.content) - 1][1]))
            else:
                if len(userdata) > 5:
                    usertext += '***' + inValue + '*** yields too many results (*'+ str(len(userdata)) +'*).\nPlease specify a more precise username'
                if len(userdata) == 0:
                    usertext += '***' + inValue + '*** doesn\'t match any known citizens.'

                em = discord.Embed(title='Citizen information', description=usertext, colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                return

    r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/players/details/'+ userId)
    obj = json.loads(r.text)

    citizen = obj['players'][userId]

    usertext = '**Status**: ' + ('Alive' if citizen['general']['is_alive'] else 'Dead') + '\n'
    usertext += '**Date registered**: ' + citizen['general']['registered'] + '\n'
    usertext += '**ID**: ' + str(citizen['citizen_id']) + '\n'
    usertext += '**Level**: ' + str(citizen['general']['level']) + '\n'
    usertext += '**Division**: ' + str(citizen['military']['division']) + '\n'
    usertext += '**Citizenship**: ' + getCountryFlag(citizen['citizenship']['country_id']) + ' ' + citizen['citizenship']['country_name'] + '\n'
    if citizen['military_unit']['name']:
        usertext += '**Military unit**: ' + citizen['military_unit']['name'] + ' ' + 'https://www.erepublik.com/en/military/military-unit/' + str(citizen['military_unit']['id']) + '\n'
    usertext += '**Strength**: ' + str(citizen['military']['strength']) + '\n'
    usertext += '**Perception**: ' + str(citizen['military']['perception']) + '\n'
    usertext += '**Rank**: ' + str(citizen['military']['rank_name']).replace('*', '\*') + '\n'
    usertext += '**Aircraft rank**: ' + str(citizen['military']['rank_name_aircraft']).replace('*', '\*') + '\n'
    if citizen['newspaper']['name']:
        usertext += '**Newspaper**: ' + citizen['newspaper']['name'] + ' ' + 'https://www.erepublik.com/en/newspaper/' + str(citizen['newspaper']['id']) + '\n'
    usertext += '**Profile link**: https://www.erepublik.com/en/citizen/profile/' + str(citizen['citizen_id']) + '\n'

    em = discord.Embed(title='Citizen information ('+ citizen['name'] +')', description=usertext, colour=0x3D9900)
    await bot.send_message(ctx.message.channel, '', embed=em)

@bot.command(pass_context=True)
async def ping(ctx):
    """Pings the bot"""
    logger.info('!ping - User: ' + str(ctx.message.author))
    em = discord.Embed(title='Pong', description='pong', colour=0x3D9900)
    await bot.send_message(ctx.message.channel, '', embed=em)

@bot.group(pass_context=True)
async def battle(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid battle command passed...')

@battle.command(pass_context=True)
async def info(ctx, battleId):
    logger.info('!battle info ' + battleId + ' - User: ' + str(ctx.message.author))
    r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/battles/details/'+ battleId)
    obj = json.loads(r.text)

    battleInfo = obj['details'][battleId]
    battleText = ''

    battleText += '**' + battleInfo['region']['name'] + '** (Round: ' + str(battleInfo['general']['round']) + ')\n'
    battleText += getCountryFlag(battleInfo['attacker']['id']) + ' **' + battleInfo['attacker']['name'] + '** [*' + str(battleInfo['attacker']['points']) + '*] - ' + getCountryFlag(battleInfo['defender']['id']) + ' **' + battleInfo['defender']['name'] + '** [*' + str(battleInfo['defender']['points']) + '*]\n'
    battleText += '**[Division 1]**  ***Wall***: *' + str(battleInfo['wall']['1']['attacker'])[0:5] + '* vs *' + str(battleInfo['wall']['1']['defender'])[0:5] + '* - ***Domination***: *' + str(battleInfo['domination']['1']['attacker']) + '* vs *' + str(battleInfo['domination']['1']['defender']) + '*\n'
    battleText += '**[Division 2]**  ***Wall***: *' + str(battleInfo['wall']['2']['attacker'])[0:5] + '* vs *' + str(battleInfo['wall']['2']['defender'])[0:5] + '* - ***Domination***: *' + str(battleInfo['domination']['2']['attacker']) + '* vs *' + str(battleInfo['domination']['2']['defender']) + '*\n'
    battleText += '**[Division 3]**  ***Wall***: *' + str(battleInfo['wall']['3']['attacker'])[0:5] + '* vs *' + str(battleInfo['wall']['3']['defender'])[0:5] + '* - ***Domination***: *' + str(battleInfo['domination']['3']['attacker']) + '* vs *' + str(battleInfo['domination']['3']['defender']) + '*\n'
    battleText += '**[Division 4]**  ***Wall***: *' + str(battleInfo['wall']['4']['attacker'])[0:5] + '* vs *' + str(battleInfo['wall']['4']['defender'])[0:5] + '* - ***Domination***: *' + str(battleInfo['domination']['4']['attacker']) + '* vs *' + str(battleInfo['domination']['4']['defender']) + '*\n'

    battleText += '**Battle link**: https://www.erepublik.com/en/military/battlefield-new/' + str(battleId) + '\n'

    em = discord.Embed(title='Battle information ('+ battleId +')', description=battleText, colour=0xBFF442)
    await bot.send_message(ctx.message.channel, '', embed=em)

@battle.command(pass_context=True)
async def co(ctx, battleId):
    logger.info('!battle co ' + battleId + ' - User: ' + str(ctx.message.author))
    r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/battles/details/'+ battleId)
    obj = json.loads(r.text)

    battleInfo = obj['details'][battleId]
    battleInfoCO = obj['details'][battleId]['combat_orders']
    battleText = ''

    battleText += '**' + battleInfo['region']['name'] + '** (Round: ' + str(battleInfo['general']['round']) + ')\n'
    battleText += getCountryFlag(battleInfo['attacker']['id']) + ' **' + battleInfo['attacker']['name'] + '** [*' + str(battleInfo['attacker']['points']) + '*] - ' + getCountryFlag(battleInfo['defender']['id']) + ' **' + battleInfo['defender']['name'] + '** [*' + str(battleInfo['defender']['points']) + '*]\n\n'
    if '1' in battleInfoCO:
        battleText += '**[Division 1]**\n'
        if '1' in battleInfoCO:
            for co in battleInfoCO['1']:
                battleText += 'Side: ' + getCountryFlag(battleInfoCO['1'][co]['country']['id']) + ' **' + battleInfoCO['1'][co]['country']['name'] + '** - Reward: *' + str(battleInfoCO['1'][co]['reward']) + '* - Budget: *' + str(battleInfoCO['1'][co]['budget']) + '* - Wall: *' + str(battleInfoCO['1'][co]['wall']) + '*\n'
        battleText += '\n**[Division 2]**\n'
        if '2' in battleInfoCO:
            for co in battleInfoCO['2']:
                battleText += 'Side: ' + getCountryFlag(battleInfoCO['2'][co]['country']['id']) + ' **' + battleInfoCO['2'][co]['country']['name'] + '** - Reward: *' + str(battleInfoCO['2'][co]['reward']) + '* - Budget: *' + str(battleInfoCO['2'][co]['budget']) + '* - Wall: *' + str(battleInfoCO['2'][co]['wall']) + '*\n'
        battleText += '\n**[Division 3]**\n'
        if '3' in battleInfoCO:
            for co in battleInfoCO['3']:
                battleText += 'Side: ' + getCountryFlag(battleInfoCO['3'][co]['country']['id']) + ' **' + battleInfoCO['3'][co]['country']['name'] + '** - Reward: *' + str(battleInfoCO['3'][co]['reward']) + '* - Budget: *' + str(battleInfoCO['3'][co]['budget']) + '* - Wall: *' + str(battleInfoCO['3'][co]['wall']) + '*\n'
        battleText += '\n**[Division 4]**\n'
        if '4' in battleInfoCO:
            for co in battleInfoCO['4']:
                battleText += 'Side: ' + getCountryFlag(battleInfoCO['4'][co]['country']['id']) + ' **' + battleInfoCO['4'][co]['country']['name'] + '** - Reward: *' + str(battleInfoCO['4'][co]['reward']) + '* - Budget: *' + str(battleInfoCO['4'][co]['budget']) + '* - Wall: *' + str(battleInfoCO['4'][co]['wall']) + '*\n'
    if '11' in battleInfoCO:
        battleText += '**[Aerial round]**\n'
        for co in battleInfoCO['11']:
            battleText += 'Side: ' + getCountryFlag(battleInfoCO['11'][co]['country']['id']) + ' **' + battleInfoCO['11'][co]['country']['name'] + '** - Reward: *' + str(battleInfoCO['11'][co]['reward']) + '* - Budget: *' + str(battleInfoCO['11'][co]['budget']) + '* - Wall: *' + str(battleInfoCO['11'][co]['wall']) + '*\n'
    battleText += '\n**Battle link**: https://www.erepublik.com/en/military/battlefield-new/' + str(battleId) + '\n'

    em = discord.Embed(title='Battle co information ('+ battleId +')', description=battleText, colour=0xBFF442)
    await bot.send_message(ctx.message.channel, '', embed=em)

@bot.group(pass_context=True)
async def history(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid history command passed...')

@history.command(pass_context=True)
async def cs(ctx, inValue : str):
    logger.info('!history cs ' + inValue + ' - User: ' + str(ctx.message.author))
    usertext = ['','','','']
    userId = ''
    userName = ''
    if is_number(inValue):
        userId = str(int(inValue))
        userName = (getUserId(userId))[0][0]
    else:
        userdata = getUser(inValue)
        if len(userdata) == 1:
            userId = str(int(userdata[0][1]))
            userName = userdata[0][0]
        else:
            if len(userdata) > 1 and len(userdata) <= 5:
                i = 1
                for citizen in userdata:
                    usertext[0] += str(i) + ') **' + citizen[0] + '** - *' + str(int(citizen[1])) + '*\n'
                    i += 1
                em = discord.Embed(title='Please enter the number of the targeted citizen', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                msg = await bot.wait_for_message(author=ctx.message.author)
                if int(msg.content) >= i or int(msg.content) < 1:
                    await bot.say('Invalid choice')
                    return
                userId = str(int(userdata[int(msg.content) - 1][1]))
                userName = userdata[int(msg.content) - 1][0]
            else:
                if len(userdata) > 5:
                    usertext[0] += '***' + inValue + '*** yields too many results (*'+ str(len(userdata)) +'*).\nPlease specify a more precise username'
                if len(userdata) == 0:
                    usertext[0] += '***' + inValue + '*** doesn\'t match any known citizens.'

                em = discord.Embed(title='Citizen history', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                return

    r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/players/history/cs/'+ userId)
    obj = json.loads(r.text)
    usertext[0] = ''
    i = 0
    hists = obj['history'][userId]['cs']
    if len(hists) > 0:
        hists = sorted(hists, key=lambda x: x['added'])
        for hist in hists:
            usertext[i] += getCountryFlag(hist['country_id_from']) + ' ***' + hist['country_name_from'] + '*** to ' + getCountryFlag(hist['country_id_to']) + ' ***' + hist['country_name_to'] + '*** on ' + hist['added'] + '\n'
            if len(usertext[i]) > 1800:
                usertext[i] += '...'
                i += 1
    else:
        usertext[0] = 'No history to display.'
    i = 0
    while len(usertext[i]):
        em = discord.Embed(title='Citizen history ('+ userName +')', description=usertext[i], colour=0x3D9900)
        await bot.send_message(ctx.message.channel, '', embed=em)
        i += 1

@history.command(pass_context=True)
async def name(ctx, inValue : str):
    logger.info('!history name ' + inValue + ' - User: ' + str(ctx.message.author))
    usertext = ['','','','']
    userId = ''
    userName = ''
    if is_number(inValue):
        userId = str(int(inValue))
        userName = (getUserId(userId))[0][0]
    else:
        userdata = getUser(inValue)
        if len(userdata) == 1:
            userId = str(int(userdata[0][1]))
            userName = userdata[0][0]
        else:
            if len(userdata) > 1 and len(userdata) <= 5:
                i = 1
                for citizen in userdata:
                    usertext[0] += str(i) + ') **' + citizen[0] + '** - *' + str(int(citizen[1])) + '*\n'
                    i += 1
                em = discord.Embed(title='Please enter the number of the targeted citizen', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                msg = await bot.wait_for_message(author=ctx.message.author)
                if int(msg.content) >= i or int(msg.content) < 1:
                    await bot.say('Invalid choice')
                    return
                userId = str(int(userdata[int(msg.content) - 1][1]))
                userName = userdata[int(msg.content) - 1][0]
            else:
                if len(userdata) > 5:
                    usertext[0] += '***' + inValue + '*** yields too many results (*'+ str(len(userdata)) +'*).\nPlease specify a more precise username'
                if len(userdata) == 0:
                    usertext[0] += '***' + inValue + '*** doesn\'t match any known citizens.'

                em = discord.Embed(title='Citizen history', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                return

    r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/players/history/name/'+ userId)
    obj = json.loads(r.text)
    usertext[0] = ''
    i = 0
    hists = obj['history'][userId]['name']
    if len(hists) > 0:
        hists = sorted(hists, key=lambda x: x['added'])
        for hist in hists:
            usertext[i] += '***' + hist['name_from'] + '*** to ***' + hist['name_to'] + '*** on ' + hist['added'] + '\n'
            if len(usertext[i]) > 1800:
                usertext[i] += '...'
                i += 1
    else:
        usertext[0] = 'No history to display.'
    i = 0
    while len(usertext[i]):
        em = discord.Embed(title='Citizen history ('+ userName +')', description=usertext[i], colour=0x3D9900)
        await bot.send_message(ctx.message.channel, '', embed=em)
        i += 1

@history.command(pass_context=True)
async def mu(ctx, inValue : str):
    logger.info('!history mu ' + inValue + ' - User: ' + str(ctx.message.author))
    usertext = ['','','','']
    userId = ''
    userName = ''
    if is_number(inValue):
        userId = str(int(inValue))
        userName = (getUserId(userId))[0][0]
    else:
        userdata = getUser(inValue)
        if len(userdata) == 1:
            userId = str(int(userdata[0][1]))
            userName = userdata[0][0]
        else:
            if len(userdata) > 1 and len(userdata) <= 5:
                i = 1
                for citizen in userdata:
                    usertext[0] += str(i) + ') **' + citizen[0] + '** - *' + str(int(citizen[1])) + '*\n'
                    i += 1
                em = discord.Embed(title='Please enter the number of the targeted citizen', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                msg = await bot.wait_for_message(author=ctx.message.author)
                if int(msg.content) >= i or int(msg.content) < 1:
                    await bot.say('Invalid choice')
                    return
                userId = str(int(userdata[int(msg.content) - 1][1]))
                userName = userdata[int(msg.content) - 1][0]
            else:
                if len(userdata) > 5:
                    usertext[0] += '***' + inValue + '*** yields too many results (*'+ str(len(userdata)) +'*).\nPlease specify a more precise username'
                if len(userdata) == 0:
                    usertext[0] += '***' + inValue + '*** doesn\'t match any known citizens.'

                em = discord.Embed(title='Citizen history', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                return

    r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/players/history/mu/'+ userId)
    obj = json.loads(r.text)
    usertext[0] = ''
    i = 0
    hists = obj['history'][userId]['mu']
    if len(hists) > 0:
        hists = sorted(hists, key=lambda x: x['added'])
        for hist in hists:
            usertext[i] += 'From ***' + (hist['mu_name_from'] + '*** https://www.erepublik.com/en/military/military-unit/' + str(hist['mu_id_from']) if hist['mu_name_from'] is not None else 'None***') + '\nTo ***' + (hist['mu_name_to'] + '*** https://www.erepublik.com/en/military/military-unit/' + str(hist['mu_id_to']) if hist['mu_name_to'] is not None else 'None***') + '\n(' + hist['added'] + ')\n'
            if len(usertext[i]) > 1800:
                usertext[i] += '...'
                i += 1
    else:
        usertext[0] = 'No history to display.'
    i = 0
    while len(usertext[i]):
        em = discord.Embed(title='Citizen history ('+ userName +')', description=usertext[i], colour=0x3D9900)
        await bot.send_message(ctx.message.channel, '', embed=em)
        i += 1

@history.command(pass_context=True)
async def party(ctx, inValue : str):
    logger.info('!history party ' + inValue + ' - User: ' + str(ctx.message.author))
    usertext = ['','','','']
    userId = ''
    userName = ''
    if is_number(inValue):
        userId = str(int(inValue))
        userName = (getUserId(userId))[0][0]
    else:
        userdata = getUser(inValue)
        if len(userdata) == 1:
            userId = str(int(userdata[0][1]))
            userName = userdata[0][0]
        else:
            if len(userdata) > 1 and len(userdata) <= 5:
                i = 1
                for citizen in userdata:
                    usertext[0] += str(i) + ') **' + citizen[0] + '** - *' + str(int(citizen[1])) + '*\n'
                    i += 1
                em = discord.Embed(title='Please enter the number of the targeted citizen', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                msg = await bot.wait_for_message(author=ctx.message.author)
                if int(msg.content) >= i or int(msg.content) < 1:
                    await bot.say('Invalid choice')
                    return
                userId = str(int(userdata[int(msg.content) - 1][1]))
                userName = userdata[int(msg.content) - 1][0]
            else:
                if len(userdata) > 5:
                    usertext[0] += '***' + inValue + '*** yields too many results (*'+ str(len(userdata)) +'*).\nPlease specify a more precise username'
                if len(userdata) == 0:
                    usertext[0] += '***' + inValue + '*** doesn\'t match any known citizens.'

                em = discord.Embed(title='Citizen history', description=usertext[0], colour=0x3D9900)
                await bot.send_message(ctx.message.channel, '', embed=em)
                return

    r = requests.get('https://api.erepublik-deutschland.de/'+ apiKey +'/players/history/party/'+ userId)
    obj = json.loads(r.text)
    usertext[0] = ''
    i = 0
    hists = obj['history'][userId]['party']
    if len(hists) > 0:
        hists = sorted(hists, key=lambda x: x['added'])
        for hist in hists:
            usertext[i] += 'From ***' + (hist['party_name_from'] + '*** https://www.erepublik.com/en/party/' + str(hist['party_id_from']) if hist['party_name_from'] is not None else 'None***') + '\nTo ***' + (hist['party_name_to'] + '*** https://www.erepublik.com/en/party/' + str(hist['party_id_to']) if hist['party_name_to'] is not None else 'None***') + '\n(' + hist['added'] + ')\n'
            if len(usertext[i]) > 1800:
                usertext[i] += '...'
                i += 1
    else:
        usertext[0] = 'No history to display.'
    i = 0
    while len(usertext[i]):
        em = discord.Embed(title='Citizen history ('+ userName +')', description=usertext[i], colour=0x3D9900)
        await bot.send_message(ctx.message.channel, '', embed=em)
        i += 1

@bot.command(pass_context=True)
async def convert(ctx, inValue : str):
    logger.info('!convert ' + inValue + ' - User: ' + str(ctx.message.author))
    
    startDate = datetime.datetime(day=21, month=11, year=2007)
    try:
        if is_number(inValue):
            delta = datetime.timedelta(days=int(inValue)-1)
            finalDate = startDate + delta
            em = discord.Embed(title='Conversion', description='Date : ' + finalDate.strftime('%d/%m/%Y'), colour=0x0053A9)
            await bot.send_message(ctx.message.channel, '', embed=em)
        else:
            inDate = datetime.datetime.strptime(inValue, '%d/%m/%Y')
            erepDay = inDate - startDate + datetime.timedelta(days=1)
            em = discord.Embed(title='Conversion', description='eRepublik day : ' + str(erepDay.days), colour=0x0053A9)
            await bot.send_message(ctx.message.channel, '', embed=em)
    except:
        traceback.print_exc()
        logger.info('Stuff broke')
        await bot.say('Stuff broke')

bot.run(config['DEFAULT']['bot_token'])
