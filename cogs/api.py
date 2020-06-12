import discord
from discord.ext import commands
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def post(session, url, data):
    async with session.post(url) as response:
        return await response.text()

class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aiosession = aiohttp.ClientSession()

    def __del__(self):
        self.aiosession.close()

def setup(bot):
    bot.add_cog(API(bot))