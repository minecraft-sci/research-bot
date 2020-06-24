import re
import discord
from discord.ext import commands


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (720725754605994087 in [y.id for y in message.author.roles]) or (720725702516932658 in [y.id for y in message.author.roles]) or message.author == self.bot.user:
            pass
        else:
            if "discord.gg/" in message.content:
                await message.delete() 


def setup(bot):
    bot.add_cog(moderation(bot))
