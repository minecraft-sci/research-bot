from discord.ext import commands
import discord
import random

class Random:
    def __init__(self, seed=6846518675):
        # initialize the math
        self.seed = seed
        self.PSeed = seed

    def next(self):
        # calculate the math
        self.seed = (self.PSeed * self.seed + 11) % 2**48
        return(self.seed)

    def randint(self, max):
        return self.next() % 100

class Maze(commands.Cog):
	def __init__(self, bot):
        # we set the rng
		self.rng = Random()
		self.bot = bot
		self.enabled = False
		self.mid = [373946864531144726]

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if ctx.author.id in self.mid and self.enabled:
			if self.rng.randint(100) == 69:
				await ctx.channel.send(f"Fuck you {ctx.author.mention}")

	@commands.has_any_role("Moderator", "Administrator", "Big Brain")
	@commands.command(name='togglemaze')
	async def togglemaze(self, ctx):
		if ctx.author.id in self.mid or ctx.author.id == 383931730211504128 or ctx.author.id == 297045071457681409: # haha my id go brrrrr
			self.enabled = not self.enabled
			await ctx.send(f"Toggled thonk responses to {self.enabled}")

def setup(bot):
	bot.add_cog(Maze(bot))
