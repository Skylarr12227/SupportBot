import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

class BitlyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.headers = {
            'Authorization': f'Bearer {self.bot.BITLY_KEY}',
            'Content-Type': 'application/json',
        }

    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command()
    async def link_metrics(self, interaction, link: str):
        """Individual link metrics for WOMBO affiliate links"""
        params = {'units': '-1'}
        ctx = await self.bot.get_context(interaction)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary',
                                   headers=self.headers,
                                   params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    clicks = data['total_clicks']
                else:
                    await ctx.send('Error retrieving link metrics.')

            async with session.get(f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
                                   headers=self.headers,
                                   params=params) as response2:
                if response2.status == 200:
                    data2 = await response2.json()
                    title = data2['title']
                    await ctx.send(f'## Title: `{title}`\n## Total clicks for `{link}`: **{clicks}**', ephemeral=True)
                else:
                    await ctx.send('Error retrieving link title.')

    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command()
    async def affiliate_board(self, interaction):
        """Affiliate leaderboard for WOMBO"""
        ctx = await self.bot.get_context(interaction)
        params = {'size': '10'}
        params2 = {'units': '-1'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api-ssl.bitly.com/v4/groups/BmbemxsY7AC/bitlinks',
                                   headers=self.headers,
                                   params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    links = data['links']
                    desc = ''
                    embed = discord.Embed(title='Bitly Link Leaderboard', color=discord.Color.blue())
                    for index, link in enumerate(links, start=1):
                        title = link['title'] or 'No Title'
                        deeplinks = link['deeplinks']
                        bitlinks = [dl['bitlink'] for dl in deeplinks]
    
                        for bitlink in bitlinks:
                            async with session.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
                                                   headers=self.headers,
                                                   params=params2) as response2:
                                if response2.status == 200:
                                    data2 = await response2.json()
                                    clicks = data2['total_clicks']
                                else:
                                    clicks = '`failed to load clicks`'
    
                                desc += f"`{index}`. **{title}**\nBitlink: {bitlink}\nClicks: {clicks}\n\n"
    
                    pages = self.pagify(desc, base_embed=embed)
                    await Paginator.Simple(ephemeral=True).start(ctx, pages=pages)
                else:
                    await ctx.send('Error retrieving link leaderboard.')

async def setup(bot):
    await bot.add_cog(BitlyCog(bot))