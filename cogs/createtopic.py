import discord
from discord.ext import commands

class createtopic(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(name="createtopic", aliases=["ctopic"])
    @commands.has_any_role("Administrator")
    async def createtopic(self, ctx, topic):
        """ Creates new topic Category """
        roleeveryone = discord.utils.get(ctx.guild.roles, name = "@everyone")
        rolemoderator = discord.utils.get(ctx.guild.roles, name = "Moderator")
        noperms = {'add_reactions': False, 'send_messages': False, 'view_channel': False, 'read_message_history': False} 
        readonlyperms = {'add_reactions': False, 'send_messages': False} 
        sendperms = {'add_reactions': True, 'send_messages': True, 'view_channel': True, 'read_message_history': True} 
        

        cat = await ctx.guild.create_category(topic)
        
        abouttc = await ctx.guild.create_text_channel("ABOUT", category=cat)
        await abouttc.set_permissions(roleeveryone, **readonlyperms)
        await abouttc.set_permissions(rolemoderator, **sendperms)

        faqtc = await ctx.guild.create_text_channel("FAQ", category=cat)
        await faqtc.set_permissions(roleeveryone, **readonlyperms)
        await faqtc.set_permissions(rolemoderator, **sendperms)

        updatestc = await ctx.guild.create_text_channel("UPDATES", category=cat)
        await updatestc.set_permissions(roleeveryone, **readonlyperms)
        await updatestc.set_permissions(rolemoderator, **sendperms)

        await ctx.guild.create_text_channel("GENERAL-DISCUSSION", category=cat)

        pdtc = await ctx.guild.create_text_channel("PRIVATE-DISCUSSION", category=cat)
        await pdtc.set_permissions(roleeveryone, **noperms)
        await pdtc.set_permissions(rolemoderator, **sendperms)

        

def setup(client):
    client.add_cog(createtopic(client))
