from discord.ext import commands
import discord
import os
from mcrcon import MCRcon

class whitelist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="rcon")
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def rcon(self, ctx):
        pass


    @rcon.command(name="whitelist")
    async def whitelist(self, ctx, name=None, discord:discord.User=None):
        """ whitelist people """
        if discord and name:
            with MCRcon("recreation.mcresear.ch", str(os.environ["RCONPW"]), 23457) as mcr:
                resp = mcr.command(f"whitelist add {name}")
                print(resp)
                await ctx.send(f"Done: {resp}")
        else:
            await ctx.send("No name/discordtag were given !rcon whitelist <NAME> <discordtag>", delete_after=8)

    @rcon.command(name="op")
    async def op(self, ctx, name=None):
        """ ops people at mc server """
        if name:
            with MCRcon("recreation.mcresear.ch", str(os.environ["RCONPW"]), 23457) as mcr:
                resp = mcr.command(f"op {name}")
                await ctx.send(f"Done: {resp}")
        else:
            await ctx.send("No name were given !rcon op <NAME>" , delete_after=8)
    
    @rcon.command(name="cmd")
    @commands.has_any_role("Administrator", "Moderator")
    async def cmd(self, ctx, *cmd):
        """ cmd at mc server """
        cmd = " ".join(cmd)
        if cmd:
            with MCRcon("recreation.mcresear.ch", str(os.environ["RCONPW"]), 23457) as mcr:
                resp = mcr.command(f"{cmd}")
                print(resp)
                await ctx.send(f"Done: {resp}")
        else:
            await ctx.send("No cmd were given !rcon cmd <CMD>", delete_after=8)

def setup(bot):
	bot.add_cog(whitelist(bot))
