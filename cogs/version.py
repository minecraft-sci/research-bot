from discord.ext import commands
import discord


class botVersion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            f = open('version', 'r')
            self.version = f.read()
        except:
            print("No version file exists")
            self.version = 'NULL'

    @commands.has_any_role("Administrator", "Moderator")
    @commands.command(name="setversion", aliases=["wvers"])
    async def setversion(self, ctx, *t_version_c):
        f = open('version', 'w+')
        t_version = ''
        for tmp in t_version_c:
            t_version += (tmp + ' ')
        f.write(str(t_version))
        # what could go wrong?
        await ctx.send(f"Succesfuly updated from {self.version} to {t_version}")
        self.version = str(t_version)


def setup(bot):
    bot.add_cog(botVersion(bot))
