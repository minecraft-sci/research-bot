from mcstatus import MinecraftServer
import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status")
    async def status(self, ctx, server='recreation.mcresear.ch'):
        ''' Query the status, ping, and user count of a given server '''
        try:
            svr = MinecraftServer.lookup(server)
            status = svr.status()
            embed = discord.Embed(title="Server Status", description=f"Server status for {server}")
            embed.add_field(name="Status", value=f"There are {status.players.online} players online right now.")
            embed.add_field(name="Server MOTD", value=status.description["text"])
            embed.add_field(name="Protocol Version", value=f"{status.version.name} : {status.version.protocol}")
            embed.add_field(name="Ping", value=f"Latency: {status.latency}ms")
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.channel.send("The server requested wasn't found or is offline.")

def setup(bot):
    bot.add_cog(Status(bot))