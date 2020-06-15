import discord
from discord.ext import commands

class tosemoji(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tosids = [722211073410727970, 722211085876461661, 722211098098532393, 722211109012111460, 722211132131115039, 722211132160344308, 722211142625394728, 722211153463476224, 722211164569993217, 722211175567196251, 722211185637982238, 722211200682950756, 722211210459873399, 722211221486436395, 722211232551141386, 722211247445246062, 722211258006503435, 722211268504584233, 722211281247141950, 722110277067210772]
        self.tos_enabled = False


    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.author, discord.User) or message.author.bot:
            return
        if ":tos:" in message.content:
            for i in range(0,20):
                if self.tos_enabled:
                    try:
                        await message.add_reaction(self.client.get_emoji(self.tosids[i]))
                    except discord.Forbidden:
                        break


    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def tostoggle(self, ctx):
        """ Toggle tos emoji reaction (If anything is in process, it will be stopped) """
        if self.tos_enabled:
            self.tos_enabled = False
        else:
            self.tos_enabled = True
        await ctx.send(f"tosemoji toggled, now: {self.tos_enabled}")


    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def tosadd(self, ctx, message: discord.Message=None):
        """ Adds tos emojis to a message (MANUALMODE) """
        if message:
            for i in range(0,20):
                try:
                    await message.add_reaction(self.client.get_emoji(self.tosids[i]))
                except discord.Forbidden:
                    break
            await ctx.send(f"Added tos emojis to message: {message.id}")


def setup(client):
    client.add_cog(tosemoji(client))