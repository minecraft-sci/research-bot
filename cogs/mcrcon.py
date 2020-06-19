from discord.ext import commands
import discord
import os
from mcrcon import MCRcon
import sqlite3

class whitelist(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.sqlitecon = sqlite3.connect('data/whitelist.db')
        self.sqlitecurs = self.sqlitecon.cursor()


    def hasWhitelisted(self, userid):
        self.sqlitecurs.execute("SELECT * FROM whitelist WHERE discorduser = ? AND valid = 1;", (userid,))
        for r in self.sqlitecurs.fetchall():
            return r[1]


    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def user(self, ctx, user:discord.User=None):
        """ returns discord user name + id """
        if user == None:
            await ctx.send("No User were given !user <DISCORDUSER>", delete_after=8)
            return
        await ctx.send(f"{user}   {user.id}")


    @commands.command()
    async def mcwhitelist(self, ctx, name=None):
        """ Adds you minecraft account to the whitelist """
        if name == None:
            await ctx.send("No name where given !mcwhitelist <IGN>", delete_after=8)
            return
        wla = self.hasWhitelisted(ctx.author.id)
        if wla:
            await ctx.send(f"You already have a account whitelisted! ign:{wla}")
            return
        with MCRcon("recreation.mcresear.ch", str(os.environ["RCONPW"]), 23457) as mcr:
                resp = mcr.command(f"whitelist add {name}")
                sm = f"Added {name} to the whitelist"
                if resp.lower() == sm.lower():
                    self.sqlitecurs.execute("INSERT INTO whitelist (discorduser, ign , valid ) VALUES (?, ?, 1);", (ctx.author.id, name,))
                    self.sqlitecon.commit()
                    await ctx.send(f"Done: {resp}")
                    return
                await ctx.send(f"{resp}", delete_after=8)


    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def mcwhitelistreset(self, ctx, user:discord.User=None):
        """ reset mcwhitelist for user """
        if user == None:
            await ctx.send("No name given !mcwhitelistreset <DISCORDUSER>", delete_after=8)
            return
        self.sqlitecurs.execute("UPDATE whitelist SET valid = 0 WHERE discorduser = ?", (user.id,))
        await ctx.send(f"whitelist command has been reseted for: {user}")
            

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def mcwhitelistget(self, ctx, user=None, active=1):
        """ whitelist debug output """
        if user == None or active not in range(0,3):
            await ctx.send("Parameters are wrong: !mcwhitelistget <IGN|DISCORD ID> [0|1|2]", delete_after=8)
            return
        if active == 2:
            self.sqlitecurs.execute("SELECT * FROM whitelist WHERE (discorduser = ? OR ign = ?);", (user,user, ))
        else:
            self.sqlitecurs.execute("SELECT * FROM whitelist WHERE (discorduser = ? OR ign = ?) AND valid = ?;", (user,user,active, ))
        await ctx.send(f"```{self.sqlitecurs.fetchall()[0:1900]}```")

	
    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def mcop(self, ctx, name=None):
        """ gives you op in minecraft """
        if name == None:
            await ctx.send("No name were given !mcop <IGN>" , delete_after=8)
            return
        with MCRcon("recreation.mcresear.ch", str(os.environ["RCONPW"]), 23457) as mcr:
            resp = mcr.command(f"op {name}")
            suc = f"Made {name} a server operator"
            if resp.lower() == suc.lower():
                await ctx.send(f"Done: {resp}")
                return
            await ctx.send(f"{resp}", delete_after=8)


    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def mcrcon(self, ctx, *cmd):
        """ rcon cmd at mc server """
        cmd = " ".join(cmd)
        if len(cmd) == 0:
            await ctx.send("No cmd were given !mcrcon <CMD>", delete_after=8)
            return
        with MCRcon("recreation.mcresear.ch", str(os.environ["RCONPW"]), 23457) as mcr:
            resp = mcr.command(f"{cmd}")
            await ctx.send(f"Done: {resp}")


def setup(bot):
	bot.add_cog(whitelist(bot))
