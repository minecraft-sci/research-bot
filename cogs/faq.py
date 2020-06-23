import discord
from discord.ext import commands
import utils.cfl as cfl
from time import time

class Faq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.code = round(time())

    def write_faq(self, itemnames, content, channels=['all'], regexes=[]):
        json_data = cfl.getConfigList("data/faq.json")
        item = {
            "names":itemnames,
            "content":content,
            "channels":channels,
            "regexes":regexes,
            "version":1
        }
        json_data.append(item)
        cfl.setConfigList(json_data, "data/faq.json")

    def fetch_faq_item(self, itemname):
        json_data = cfl.getConfigList("data/faq.json")
        for item in json_data:
            if itemname in item["names"]:
                return item
        return None

    @commands.command(name="faq")
    async def faq(self, ctx, subcommand=None):
        ''' Shows items of the FAQ from the faq.json file '''
        if subcommand == None:
            pass
        faq_item = self.fetch_faq_item(subcommand)
        if faq_item:
            await ctx.channel.send(faq_item["content"])
        else:
            faq_data = cfl.getConfigList("data/faq.json")
            data = "FAQ Commands:```"
            for i in faq_data:
                data += i["names"][0]
            await ctx.channel.send(f"{data}```")

    @commands.group(name="faqmod")
    @commands.has_any_role("Administrator", "Moderator")
    async def faqmod(self, ctx):
        ''' moderation commands for the FAQ '''
        if ctx.invoked_subcommand == None:
            pass

    @faqmod.command(name="add")
    async def faqmod_add(self, ctx):
        ''' add FAQ entries '''
        args = ctx.message.content.split("\n")[1:]
        names = args[0].split()
        content = args[1]
        regexes = args[2].split("   ")
        if len(regexes) < 1 or regexes[0].lower() == 'none':
            regexes = []
        channels = args[3].split()
        allow = True
        denied_names = []
        for name in names:
            if self.fetch_faq_item(name):
                allow = False
                denied_names.append(name)
        if allow:
            await ctx.channel.send(f"```To add:\nNames: {names}\nContent: {content}\nRegexes: {regexes}\nChannels: {channels}```")
        else:
            await ctx.channel.send(f"```To add:\nNames: {names}\nContent: {content}\nRegexes: {regexes}\nChannels: {channels}\n\nThese could not be added due to name conflicts: {denied_names}\nPlease resolve these naming issues to add the FAQ entry.```")
        self.write_faq(names, content, channels, regexes)

    @faqmod.command(name="get")
    async def faqmod_get(self, ctx, name):
        item = self.fetch_faq_item(name)
        if not item:
            await ctx.channel.send(f"'{name}' is not a valid FAQ command.")
        else:
            await ctx.channel.send(f"```Names: {item['names']}\nContent: {item['content']}\nRegexes: {item['regexes']}\nChannels: {item['channels']}```")

    @faqmod.command(name="del", aliases=["delete"])
    @commands.has_any_role("Administrator")
    async def faqmod_del(self, ctx, name, code:int=None):
        if not code:
            await ctx.channel.send(f"Run this command again with the code {self.code} to confirm deletion.")
            return
        if not code == self.code:
            await ctx.channel.send(f"The code you used was incorrect, please use {self.code}")
            return
        else:
            self.code = round(time())
            json_data = cfl.getConfigList("data/faq.json")
            item = self.fetch_faq_item(name)
            if item:
                json_data.pop(json_data.index(item))
                cfl.setConfigList(json_data, "data/faq.json")
                await ctx.channel.send(f"Successfully deleted FAQ entry for {name}")
            else:
                await ctx.channel.send(f"That FAQ entry wasn't found. Please rerun the command with the correct name and the code {self.code}")

def setup(bot: commands.Bot):
    bot.add_cog(Faq(bot))