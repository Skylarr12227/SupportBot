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


    @app_commands.command()
    async def affiliate_board(self, interaction):
        """Affiliate leaderboard for WOMBO"""
        ctx = await self.bot.get_context(interaction)
        params = {'size': '10'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api-ssl.bitly.com/v4/groups/BmbemxsY7AC/bitlinks',
                                   headers=self.headers,
                                   params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    links = data['links']

                    embed = discord.Embed(title='Bitly Link Leaderboard', color=discord.Color.blue())
                    for index, link in enumerate(links, start=1):
                        title = link['title'] or 'No Title'
                        try:
                            clicks = link['links']
                        except:
                            clicks = "Error loading clicks"
                        embed.add_field(name=f'{index}. {title}', value=f'Clicks: {clicks}', inline=False)

                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    await ctx.send(f'Error: {response}')

async def setup(bot):
    await bot.add_cog(BitlyCog(bot))