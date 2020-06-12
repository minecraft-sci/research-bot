import discord
from discord.ext import commands

from dotenv import load_dotenv
import os
load_dotenv("./secrets/.env")

client = commands.Bot(command_prefix="!")

cogs = [
    "cogs.general"
]

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("Starting bot.")
    try:
        client.run(os.environ["TOKEN"])
    except Exception as e:
        print("Login failed. Invalid token?")