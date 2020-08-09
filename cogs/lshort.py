import discord
from discord.ext import commands
import os
import pyourls3

class LShort(commands.Cog):

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
                if url.startswith("https://mcatho.me") or url.startswith("http://mcatho.me") or url.startswith("mcatho.me"):
                    await ctx.send("I refuse to do that because you are stupid!")
                    return
                else:
                    surl = self.yourls.shorten(url, keyword=short)
            await ctx.send(f"URL got shorten:\nLong URL:```{surl['url']['url']}```Short URL:```{surl['shorturl']}```")
        except:
            await ctx.send(f"The keyword probably already exists! \"{short}\", delete_after=10)

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def urlstats(self, ctx, url=None):
        """ Get Stats from shortened URL's """
        if url == None:
            await ctx.send("Usage: !urlstats <keyword/shorturl | all>")
            return
        if url == "all":
            urls = self.yourls.stats()
            await ctx.send(f"General link statistics:\nTotal Links: ```{urls['total_links']}```Total Clicks:```{urls['total_clicks']}```")
        else:
            try:
                urls = self.yourls.url_stats(url)
                await ctx.send(f"Stats for shortened URL:```{urls['shorturl']}```Long URL:```{urls['url']}```Clicks:```{urls['clicks']}```Created:```{urls['timestamp']}```")
            except:
                await ctx.send(f"The keyword/shorturl probably doesn't exist! `{url}`", delete_after=10)

def setup(client):
    client.add_cog(LShort(client))
