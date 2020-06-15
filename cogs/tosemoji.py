import discord
from discord.ext import commands

class tosemoji(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tosids = [722190352043212893, 722190367205883974, 722190379658772596, 722190395311784007, 722190409035677800, 722190420972404757, 722190434276737024, 722190449694998618, 722190461669998664, 722190473854451786, 722190486219259914, 722190497485029534, 722190507928715337, 722190519047946250, 722190528719880333, 722190539641847860, 722190550995959889, 722190561859338292, 722190573653590036, 722190584210653236]
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