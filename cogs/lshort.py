import discord
from discord.ext import commands
import os
import pyourls3

class lshort(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.yourls = pyourls3.Yourls('https://mcatho.me/yourls-api.php', user='bot', passwd=os.environ["YOURLSPW"])

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def shorturl(self, ctx, url, short=None):
        """ creates a short mcatho.me url """
        try:
            if (short == None):
                surl = self.yourls.shorten(url)
            else:
                surl = self.yourls.shorten(url, keyword=short)
            await ctx.send("URL got shorten:\nLong URL:```"+surl['url']['url']+"```Short URL:```"+surl['shorturl']+"```")
        except:
            await ctx.send("The keyword probably already exists! `"+short+"`", delete_after=10)

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def urlstats(self, ctx, url):
        """ Get Stats from shortend URL's """
        if url == "all":
            urls = self.yourls.stats()
            await ctx.send("General link statistics:\nTotal Links: ```"+urls['total_links']+"```Total Clicks:```"+urls['total_clicks']+"```")
        else:
            urls = self.yourls.url_stats(url)
            await ctx.send("Stats for shortened URL:```"+urls['shorturl']+"```Long URL:```"+urls['url']+"```Klicks:```"+urls['clicks']+"```Created:```"+urls['timestamp']+"```")

def setup(client):
    client.add_cog(lshort(client))