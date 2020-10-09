from discord.ext import commands

from cogs.adminonly import is_admin


class BaseCommands(commands.Cog):
    """
    This class contains essential commands, that should not be unloaded when other commands need to be changed,
    therefore are in a separate file.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["l"])
    @commands.check(is_admin)
    async def load(self, ctx, extension):
        """
        Loads a discord.py cog
        :param ctx: The Context object, it's passed automatically
        :param extension: The name of the cog to be loaded
        """
        self.bot.load_extension(extension)
        await ctx.message.delete()
        await ctx.send(f"Loaded {extension} :white_check_mark:", delete_after=5)

    @commands.command(aliases=["uload", "ul"])
    @commands.check(is_admin)
    async def unload(self, ctx, extension):
        """
        Unloads a discord.py cog
        :param ctx: The Context object, it's passed automatically
        :param extension: The name of the cog to be unloaded
        """
        await ctx.message.delete()
        self.bot.unload_extension(extension)
        await ctx.send(f"Unloaded {extension} :white_check_mark:", delete_after=5)


def setup(bot):
    bot.add_cog(BaseCommands(bot))
