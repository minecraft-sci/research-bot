from discord.ext import commands
import discord
import os
from mcrcon import MCRcon
import utils.cfl as cfl

class whitelist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def hasWhitelisted(self, userID):
        json_data = cfl.getConfigList("data/whitelist.json")
        for item in json_data:
            if item["sender"] == userID:
                return True
        return False

    @commands.group(name="rcon")
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def rcon(self, ctx):
        pass

    @rcon.command(name="whitelist")
    async def whitelist(self, ctx, name=None, discord:discord.User=None):
        """ whitelist people """
        if self.hasWhitelisted(ctx.author.id):
            await ctx.channel.send("You have already used this command the maximum of 1 times!")
            return
        if discord and name:
            with MCRcon("recreation.mcresear.ch", str(os.environ["RCONPW"]), 23457) as mcr:
                resp = mcr.command(f"whitelist add {name}")
                print(resp)
                await ctx.send(f"Done: {resp}")
                if resp.lower() == f"Added {name} to the whitelist":
                    json_data = cfl.getConfigList("data/whitelist.json")
                    json_data.append({"name":name, "user":str(discord), "sender":ctx.author.id})
                    cfl.setConfigList(json_data, "data/whitelist.json")
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

    @rcon.command(name="resetlimit")
    @commands.has_any_role("Moderator", "Administrator")
    async def resetlimit(self, ctx, user: discord.User = None):
        if user:
            json_data = cfl.getConfigList("data/whitelist.json")
            for i, item in enumerate(json_data):
                if item["sender"] == user.id:
                    json_data.pop(i)
                    await ctx.channel.send(f"Reset whitelist limit for {user}")
                    cfl.setConfigList(json_data, "data/whitelist.json")
                    return
            await ctx.channel.send(f"User {user} was not found in the whitelist cache!")
        else:
            await ctx.channel.send("No user was specified. !rcon resetlimit <user>")

def setup(bot):
	bot.add_cog(whitelist(bot))
