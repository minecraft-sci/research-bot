import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

class Query:
    def __init__(self, url="https://minecraftathome.com/minecrafthome/top_users.php"):
        self.url = url

    def getLeaderboards(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")
        table = soup.findAll("table")[0].get_text()
        table_lines = table.split("\n")

        person = []
        avg = []
        total = []

        a = 4

        for i, item in enumerate(table_lines):
            if i < 3 or a >= len(table_lines):
                pass
            else:
                person.append(table_lines[a])
                avg.append(table_lines[a+1])
                total.append(table_lines[a+2])
                a += 8

        return zip(person, avg, total)



class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lb", aliases=["leaderboard", "top"])
    async def leaderboard(self, ctx):
        embed = discord.Embed(title="MC@H Leaderboard", description="Top 12 MC@H users", color=0x3AF13A)
        d = 0
        for a, b, c in Query().getLeaderboards():
            if d < 12:
                d += 1
                embed.add_field(name=f"{d+1}) {a[1:]}", value=f"Recent average: {b}\nTotal Credit: {c}")
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Leaderboard(bot))