import struct
import discord
from discord.ext import commands


class SeedUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="validseed", aliases=["vs"])
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def validseed(self, ctx, wowthiswasnotfun):
        try:
            worldSeed = int(wowthiswasnotfun)
            if worldSeed > 0:
                upperBits = worldSeed >> 32
            else:
                upperBits = (worldSeed >> 32)+(2 << 31)
            lowerBits = worldSeed & ((1 << 32)-1)
            a = (24667315 * upperBits + 18218081 * lowerBits + 67552711) >> 32
            b = (-4824621 * upperBits + 7847617 * lowerBits + 7847617) >> 32
            seed = 7847617 * a - 18218081 * b
            if seed > 0:
                if(((seed * 25214903917 + 11) & ((1 << 48) - 1))) > 0:
                    nextLong = ((struct.unpack("@q", struct.pack("@Q", (seed >> 16 << 32)))[0]) + (
                        ((seed * 25214903917 + 11) & ((1 << 48) - 1)) >> 16) % -2147483648)
                    nextLong2 = ((struct.unpack("@q", struct.pack("@Q", (seed >> 16 << 32)))[0]) + (
                        ((seed * 25214903917 + 11) & ((1 << 48) - 1)) >> 16) % 2147483648)
                else:
                    nextLong = (
                        (seed >> 16 << 32) + ((((seed * 25214903917 + 11) & ((1 << 48) - 1)) >> 16))+(2 << 15))
            else:
                if(((seed * 25214903917 + 11) & ((1 << 48) - 1))) > 0:
                    nextLong = (((((seed >> 16)+(2 << 15)) << 32)) +
                                (((seed * 25214903917 + 11) & ((1 << 48) - 1)) >> 16))
                else:
                    nextLong = (((((seed >> 16)+(2 << 15)) << 32)) +
                                ((((seed * 25214903917 + 11) & ((1 << 48) - 1)) >> 16))+(2 << 15))
            if(nextLong != worldSeed):
                if(nextLong2 == worldSeed):
                    await ctx.channel.send("Valid Seed")
                    return
                else:
                    await ctx.channel.send("Invalid Seed")
                    return
            elif(nextLong == worldSeed):
                await ctx.channel.send("Valid Seed")
                return
        except:
            await ctx.channel.send("Invalid seed")

    @commands.command(name="sisterseed", aliases=["sis"])
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def sisterseed(self, ctx, theseed):
        def modInverse(a, k):
            x = ((((a << 1) ^ a) & 4) << 1) ^ a
            x += x - a * x * x
            x = x % 9223372036854775808
            x += x - a * x * x
            x = x % -9223372036854775808
            x += x - a * x * x
            x = x % -9223372036854775808
            x += x - a * x * x
            x = x % -9223372036854775808
            return x & -1
        seed1 = int(theseed)
        if(seed1 < 0):
            await ctx.channel.send(((-1442695040888963407 * modInverse(6364136223846793005, 64)) - seed1) % -9223372036854775808)
        else:
            await ctx.channel.send(((-1442695040888963407 * modInverse(6364136223846793005, 64)) - seed1) % 9223372036854775808)


def setup(bot):
    bot.add_cog(SeedUtils(bot))