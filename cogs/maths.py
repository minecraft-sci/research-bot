import discord
from discord.ext import commands

class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="=")
    async def evaulate(self, ctx, *expr):
        expr = " ".join(expr)
        try:
            result = eval(expr)
            embed = discord.Embed(title=expr)
            embed.add_field(name="Result", value=f"{result}")
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.channel.send(f"Evaluation of {expr} failed.")

def setup(bot):
    bot.add_cog(Maths(bot))