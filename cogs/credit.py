# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
from pathlib import Path
import json

help_data = """Credit commands
`!credit createproject <project_name>` - admin only
`!credit create <project_name> <discord.Member> [minecraft_ign]`
`!credit add <project_name> <discord.Member> <give credit for something>`
`!credit top <project_name> <discord.Member> <a new top contribution>`
`!credit dump <project_name>`
"""

class Credit(commands.Cog):
    """Credit users the real way"""

    def __init__(self, bot):
        self.bot = bot

    def get_users(self, project):
        path = Path(f"./data/proj_{project}.json")
        with path.open() as f:
            return json.load(f)

    def get_user(self, uid, project):
        data = self.get_users(project)
        for item in data:
            if item["discord_id"] == uid:
                return item

    async def success(self, ctx):
        await ctx.channel.send("Operation completed successfully :ok_hand:")

    @commands.group(name="credit")
    @commands.has_any_role("Big Brain", "Moderator", "Administrator")
    async def credit(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.channel.send(help_data, delete_after=30)

    @credit.command(name="createproject", aliases=["cp", "cproj"])
    @commands.has_any_role("Administrator")
    async def cproject(self, ctx, name):
        path = Path(f"./data/proj_{name}.json")
        if path.exists():
            await ctx.channel.send("There is already a project with that name!")
            return
        with path.open("w") as f:
            f.write("[]")
        await ctx.channel.send(f"Created project {name} successfully!")

    @credit.command(name="give")
    async def cgive(self, ctx, project, user: discord.Member, *contrib):
        contrib = " ".join(contrib)
        if not Path(f"./data/proj_{project}.json").exists():
            await ctx.channel.send("The project name you have entered is invalid!")
            return
        if not self.get_user(user.id, project):
            await ctx.channel.send(f"This user has not yet been created, please use `!credit create {project} <user> [mcname]`")
        data = self.get_users(project)
        for i, item in enumerate(data):
            if item["discord_id"] == user.id:
                data[i]["contributions"].append(contrib)
        with Path(f"./data/proj_{project}.json").open("w") as f:
            json.dump(data, f)
        await self.success(ctx)

    @credit.command(name="create")
    async def create(self, ctx, project, user: discord.Member, mcname=None):
        if not Path(f"./data/proj_{project}.json").exists():
            await ctx.channel.send("The project name you have entered is invalid!")
            return
        if self.get_user(user.id, project):
            await ctx.channel.send("This user has already been reated, did you mean `!credit give`?")
            return
        path = Path(f"./data/proj_{project}.json")
        user = {
            "discord_id":user.id,
            "discord_tag":str(user),
            "minecraft_username":mcname,
            "contributions":[],
            "main_contribution":""
        }
        data = self.get_users(project)
        data.append(user)
        with path.open("w") as f:
            json.dump(data, f)
        await self.success(ctx)

    @credit.command(name="top", aliases=["main"])
    async def give(self, ctx, project, user: discord.Member, *contrib):
        contrib = " ".join(contrib)
        if not Path(f"./data/proj_{project}.json").exists():
            await ctx.channel.send("The project name you have entered is invalid!")
            return
        if not self.get_user(user.id, project):
            await ctx.channel.send(f"This user has not yet been created, please use `!credit create {project} <user> [mcname]`")
        data = self.get_users(project)
        for i, item in enumerate(data):
            if item["discord_id"] == user.id:
                data[i]["main_contribution"] = contrib
        with Path(f"./data/proj_{project}.json").open("w") as f:
            json.dump(data, f)
        await self.success(ctx)

    @credit.command(name="dump")
    async def dump(self, ctx, project, fmt="json"):
        if not Path(f"./data/proj_{project}.json").exists():
            await ctx.channel.send("The project name you have entered is invalid!")
            return
        if fmt == "json":
            with Path(f"./data/proj_{project}.json").open() as f:
                await ctx.channel.send(file=discord.File(f, filename="contributors.json"))

    @credit.command(name="user")
    async def cuser(self, ctx, project, user: discord.Member = None):
        if not Path(f"./data/proj_{project}.json").exists():
            await ctx.channel.send("The project name you have entered is invalid!")
            return
        if not user:
            user = ctx.author
        data = self.get_user(user.id, project)
        embed = discord.Embed(title="User Crediting", description=f"Report for {user}")
        embed.add_field(name="Top Contribution", value=data["main_contribution"]) if data["main_contribution"] else None
        contribs = "\n".join(data["contributions"])
        embed.add_field(name="Contributions", value=contribs) if contribs else None
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Credit(bot))
