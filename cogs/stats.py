# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import json
import time
from pathlib import Path

def getHour():
    return time.time() // 3600

class Stats(commands.Cog):
    """Multipurpose statistics tracking for MC@H"""

    def __init__(self, bot):
        self.bot = bot
        self.updates = 0
        self.uthresh = 10
        self.createIfNotExist()
        self.channel_data = self.getData("channels")
        self.smcount_data = self.getData("members")

    def createIfNotExist(self):
        channels = Path("data/channels.json")
        members = Path("data/members.json")
        if not channels.exists():
            with channels.open("w") as f:
                json.dump([], f)
        if not members.exists():
            with members.open("w") as f:
                json.dump([], f)

    def getData(self, name):
        with Path(f"data/{name}.json").open() as f:
            return json.load(f)

    def setData(self, name, data):
        with Path(f"data/{name}.json").open("w") as f:
            json.dump(data, f)

    def update(self):
        self.updates += 1
        if self.updates % self.uthresh:
            self.setData("channels", self.channel_data)
            self.setData("members", self.smcount_data)

    def hasHour(self, data, hour):
        for item in data:
            if item["hour"] == hour:
                return True
        return False

    def channelMessage(self, channelid, content):
        hour = getHour()
        data = {"time": round(time.time()), "content": content}
        if not self.hasHour(self.channel_data, hour):
            self.channel_data.append({"hour":hour, "messages":[data]})
        else:
            for i, item in enumerate(self.channel_data):
                if item["hour"] == hour:
                    self.channel_data[i]["messages"].append(data)
        self.update()

    def memberUpdate(self, typ):
        self.smcount_data.append({"time": round(time.time()), "type": typ})
        self.update()


    @commands.Cog.listener()
    async def on_message(self, message):
        self.channelMessage(message.channel.id, message.content)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.memberUpdate("join")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.memberUpdate("leave")

def setup(bot):
    bot.add_cog(Stats(bot))
