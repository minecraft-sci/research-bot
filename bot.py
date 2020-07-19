import discord
from discord.ext import commands

from dotenv import load_dotenv
import os
import sys
load_dotenv("./secrets/.env")

client = commands.Bot(command_prefix="!")
client.remove_command("help")

cogs = [
    "cogs.moderation",
    "cogs.general",
    "cogs.createtopic",
    "cogs.tos",
    "cogs.tosemoji",
    #"cogs.mcrcon",
    "cogs.maze",
    "cogs.faq",
    "cogs.serverstatus",
    "cogs.leaderboard"
]

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print(e)

@client.command()
@commands.has_any_role("Moderator", "Administrator")
async def reload(ctx):
    """ Reload all extensions """
    for exten in cogs:
        try:
            client.reload_extension(exten)
        except Exception as e:
            print(e)
    await ctx.send("Reload Succesful")

@client.command()
@commands.has_any_role("Moderator", "Administrator")
async def restart(ctx):
    """ Restart the bot """
    await client.close()
    os.system('echo "sleep 10; kill $PPID" |at now')
    exit(69)

if __name__ == "__main__":
    print("Starting bot.")
    try:
        client.run(os.environ["TOKEN"])
    except Exception as e:
        print("Login failed. Invalid token?")
