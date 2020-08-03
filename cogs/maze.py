from discord.ext import commands
import discord
import random
class Maze(commands.Cog):
	def __init__(self, bot):
		self.rng = random
		self.bot = bot
        # we define the enablement toggle
		self.enabled = True
		self.mid = [373946864531144726]
		self.nooooooooo = [738981683516145785]

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if ctx.author.id in self.mid and self.enabled:
            # here it go brrrr
			if self.rng.randint(0,100) == 42:
				await ctx.channel.send(f"Fuck you {ctx.author.mention}")
			if self.rng.randint(0,100) == 69:
				await ctx.channel.send(f"Do you like Alex Dillinger {ctx.author.mention}")
				
		if ctx.author.id in self.nooooooooo and self.enabled:
			# Why are you taking this risk?
			# -> Yes.
			
			if self.rng.randint(1,100) in [7,77]:
				await ctx.channel.send(f"Ewww cringe. {ctx.author.mention}")
		

	@commands.group(name="maze")
	async def maze(self, ctx):
		pass

	@maze.command(name='toggle') # What is the point in commands.has_any_role if it checks by id anyway?
	async def togglemaize(self, ctx):
		if ctx.author.id in self.mid or ctx.author.id in [383931730211504128,297045071457681409,738981683516145785]: # haha my id go brrrrr, haha my id also go brrrrr
			self.enabled = not self.enabled
			await ctx.send(f"Toggled thonk responses to {self.enabled}")

def setup(bot):
	bot.add_cog(Maze(bot))
