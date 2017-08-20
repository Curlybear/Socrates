import discord
from discord.ext import commands
import logging
import json

import ereputils

logger = logging.getLogger('Socrates.Wiki')


class Wiki:
    def __init__(self, bot):
        self.bot = bot
        self.utils = ereputils.ErepUtils()

    @commands.command(pass_context=True, aliases=['ALLIANCES'])
    async def alliances(self, ctx):
        logger.info('!alliances - User: ' + str(ctx.message.author))
        await self.bot.send_file(ctx.message.channel, 'img/alliances.png')

    @commands.command(pass_context=True, aliases=['WIKI'])
    async def wiki(self, ctx, *, search_query):
        logger.info('!wiki ' + search_query + ' - User: ' + str(ctx.message.author))
        data = self.utils.search_wiki(search_query)

        if len(data) == 1:
            result_id = 0
        else:
            if 1 < len(data) <= 10:
                # Display all results then await choice
                i = 1
                text = ''
                for entry in data:
                    text += str(i) + ') **' + entry[1] + '** - *Category: ' + str(entry[2]) + '*\n'
                    i += 1
                em = discord.Embed(title='Please enter the number of the targeted wiki entry',
                                   description=text,
                                   colour=0x3D9900)
                await self.bot.send_message(ctx.message.channel, '', embed=em)
                msg = await self.bot.wait_for_message(author=ctx.message.author)
                if int(msg.content) >= i or int(msg.content) < 1:
                    await self.bot.say('Invalid choice')
                    return
                result_id = int(msg.content) - 1
            else:
                await self.bot.send_message(ctx.message.channel, 'No matching entry found.')
                return
        temp = json.JSONDecoder().decode(data[result_id][3])
        tempembed = discord.Embed().from_data(temp)
        await self.bot.send_message(ctx.message.channel, '', embed=tempembed)

    @commands.command(pass_context=True, aliases=['WIKICATS'])
    async def wikicats(self, ctx):
        data = self.utils.get_wiki_categories()
        data.sort()
        text = ''
        for category in data:
            text += ':small_orange_diamond:' + category[0].title() + '\n'
        embed = discord.Embed(title="Wiki categories",
                              description=text,
                              color=0x808000)
        await self.bot.send_message(ctx.message.channel, '', embed=embed)

    @commands.command(pass_context=True, aliases=['WIKILIST'])
    async def wikilist(self, ctx, *, category):
        data = self.utils.get_wiki_entries_for_category(category)
        data.sort()
        text = ''
        for entries in data:
            text += ':small_orange_diamond:' + entries[0].title() + '\n'
        embed = discord.Embed(title='Wiki entries for category: \"' + category + '\"',
                              description=text,
                              color=0x808000)
        await self.bot.send_message(ctx.message.channel, '', embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))
