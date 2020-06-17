import discord
from discord.ext import commands

from dotenv import load_dotenv
import os
import sys
load_dotenv("./secrets/.env")

client = commands.Bot(command_prefix="!")
client.remove_command("help")

cogs = [
    "cogs.general",
    "cogs.createtopic",
    "cogs.api",
    "cogs.tos",
    "cogs.tosemoji",
    "cogs.maze"
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
    sys.exit(64)

if __name__ == "__main__":
    print("Starting bot.")
    try:
        client.run(os.environ["TOKEN"])
    except Exception as e:
        print("Login failed. Invalid token?")