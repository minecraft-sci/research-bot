import discord
from discord.ext import commands
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(), response.status

async def post(session, url, data):
    async with session.post(url) as response:
        return await response.text(), response.status

class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aiosession = aiohttp.ClientSession()

    def __del__(self):
        self.aiosession.close()

    @commands.group(name="api")
    @commands.has_any_role("Moderator", "Administrator")
    async def api(self, ctx):
        pass

    @api.command(name="get")
    async def api_get(self, ctx, url, mode='all'):
        data = await fetch(self.aiosession, url)
        embed = discord.Embed(title="API Test", description=f"API Test data for {url}")
        if mode == 'all':
            embed.add_field(name="Status Code", value=data[1])
            embed.add_field(name="Response Data", value=data[0]) if len(data[0]) < 1023 else embed.add_field(name="Response Data", value="Too much content.")
        elif mode == 'status':
            embed.add_field(name="Status Code", value=data[1])
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(API(bot))