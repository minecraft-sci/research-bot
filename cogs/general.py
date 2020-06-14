import utils.savestats as stats
import utils.cfl as cfl

import discord
from discord.ext import commands
import time


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.initTime = round(time.time())

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="on Minecraft Research"))

    @commands.command(name="info")
    @commands.has_any_role("Member", "Moderator", "Administrator")
    async def info(self, ctx):
        embed = discord.Embed(title="Research Bot Info",
                              description="Useful info and stats for ResBot")
        uptime = round(time.time() - self.initTime)
        hours = uptime // 3600
        minutes = (uptime - (hours * 3600)) // 60
        seconds = uptime - (hours * 3600 + minutes * 60)
        embed.add_field(
            name="Uptime", value=f"{hours} hours, {minutes} minutes, {seconds} seconds")

        # yes, IK about DRY, and it is here so that the bot won't need to be restarted/reloaded for the verison number to update
        try:
            f = open('version', 'r')
            version = f.read()
        except:
            print("No version file exists")
            version = 'NULL'

        embed.add_field(
            name="Version", value=f"Currently running {str(version)}")
            
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))