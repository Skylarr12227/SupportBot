import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
import Paginator
from supportbot.core.utils import team, support


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

    @support()
    @app_commands.command()
    async def affiliate_board(self, interaction):
        """Affiliate leaderboard for WOMBO"""
        ctx = await self.bot.get_context(interaction)
        params = {'size': '10'}
        params2 = {'units': '-1'}
        def pagify(text: str, *, per_page: int = 15, sep: str = "\n", base_embed=None):
            page = ""
            pages = []
            raw = text.strip().split(sep)
            total_pages = ((len(raw) - 1) // per_page) + 1
            for idx, part in enumerate(raw):
                page += part + sep
                if idx % per_page == per_page - 1 or idx == len(raw) - 1:
                    # Strip out the last sep
                    page = page[: -len(sep)]
                    if base_embed is not None:
                        embed = base_embed.copy()
                        embed.description = page
                        embed.set_footer(text=f"Page {(idx // per_page) + 1}/{total_pages}")
                        pages.append(embed)
                    else:
                        pages.append(page)
                    page = ""
            return pages

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
                        bitlink = link['id']
                        
                    
                        async with session.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
                                   headers=self.headers,
                                   params=params2) as response2:
                            if response2.status == 200:
                                data2 = await response2.json()
                                clicks = data['total_clicks']
                            else:
                                clicks = '`failed to load clicks`'
                        desc += f"`{index}`. **{title}**',\nClicks: {clicks}"            

                    pages = pagify(desc, base_embed=embed)
                    await Paginator.Simple(ephemeral=True).start(ctx, pages=pages)
                    #await ctx.send(embed=embed)
                else:
                    await ctx.send('Error retrieving link leaderboard.')

    @support()
    @app_commands.command()
    async def create_bitly(self, interaction, url: str, title: str):
        """Create a Bitly link"""
        ctx = await self.bot.get_context(interaction)
        data = {
            'group_guid': 'BmbemxsY7AC',
            'domain': 'wombo.com',
            'long_url': url,
            'title': title
        }
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api-ssl.bitly.com/v4/bitlinks',
                                    headers=self.headers,
                                    json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    bitlink = data['link']
                    await ctx.send(f'Bitly link created: {bitlink}', ephemeral=True)
                elif response.status == 400:
                    await ctx.send('Invalid URL or title. Please check the URL and title and try again.', ephemeral=True)
                elif response.status == 401:
                    await ctx.send('Invalid Bitly API key. Please check the API key and try again.', ephemeral=True)
                elif response.status == 429:
                    await ctx.send('Rate limit exceeded. Please try again later.', ephemeral=True)
                else:
                    data = await response.json()
                    formatted_data = '\n'.join(f'{k}: {v}' for k, v in data.items())
                    await ctx.send(response)

async def setup(bot):
    await bot.add_cog(BitlyCog(bot))
