# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
from mcrcon import MCRcon
from dotenv import load_dotenv
import os

load_dotenv("./secrets/.env")

class Rcon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.mcr = MCRcon(os.environ["rcon_ip"], os.environ["rcon_pass"], int(os.environ["rcon_port"]))
        self.mcr.connect()

    async def send_resp(self, resp: str, ctx: commands.Context):
        if str(resp) == "":
            await ctx.channel.send("There was no response text for this command execution.")
            return
        await ctx.channel.send(resp)

    @commands.group(name="rcon")
    async def rcon(self, ctx):
        self.mcr.command(f"//;{ctx.message.content}")

    @rcon.command(name="exec")
    @commands.has_any_role("Moderator", "Administrator")
    async def rcon_exec(self, ctx, *command):
        command = " ".join(command)
        resp = self.mcr.command(command)
        await self.send_resp(resp, ctx)

    @rcon.command(name="whitelist")
    @commands.has_any_role("Big Brain", "Moderator", "Administrator", "Developer")
    async def rcon_whitelist(self, ctx, ign, typ="allow"):
        if typ == "allow":
            resp = self.mcr.command(f"whitelist add {ign}")
            await self.send_resp(resp, ctx)
        else:
            resp = self.mcr.command(f"whitelist remove {ign}")
            await self.send_resp(resp, ctx)


def setup(bot):
    bot.add_cog(Rcon(bot))
