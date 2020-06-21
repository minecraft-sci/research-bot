import utils.savestats as stats
import utils.cfl as cfl

import discord
from discord.ext import commands
import time

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.initTime = round(time.time())

    async def presence_update(self):
        guild = self.bot.get_guild(720723932738486323)
        if guild:
            await self.bot.change_presence(activity=discord.Game(name=f"{guild.member_count} users"))
            return
        await self.bot.change_presence(activity=discord.Game(name="Minecraft@Home"))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.presence_update()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.presence_update()

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        await self.presence_update()

    @commands.command(name="info")
    @commands.has_any_role("Member", "Moderator", "Administrator")
    async def info(self, ctx):
        embed = discord.Embed(title="Research Bot Info", description="Useful info and stats for ResBot")
        uptime = round(time.time() - self.initTime)
        hours = uptime // 3600
        minutes = (uptime - (hours * 3600)) // 60
        seconds = uptime - (hours * 3600 + minutes * 60)
        embed.add_field(name="Uptime", value=f"{hours} hours, {minutes} minutes, {seconds} seconds")
        version = cfl.getConfigAttribute("version", "static_data/version-inf.json")
        rel_type = cfl.getConfigAttribute("release", "static_data/version-inf.json")
        embed.add_field(name="Version", value=f"{version} {rel_type}")
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))