import datetime
import random
import discord
from discord.ext import commands


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def changelog(self, ctx):
        """Prints what's new in this version"""
        await ctx.send("-Updated the discord.py library version\n-The Bot class has been rewritten")
        await ctx.message.delete()

    # bulk delete, hogy a ?clear ne triggerelje az on_message_delete eventet
    # TODO: check if amount is positive
    @commands.command(aliases=["delete", "del", "c", "clear", "purge"])
    # amount a törlendő üzenetek száma 
    # (3 a minimum, mert magát a commandot és legalább az utolsó 2 másik üzenetet töröljük)
    async def bulkdel(self, ctx, amount: str = "2"):
        """Updated version of ?clear. Deletes a given amount of messages, default is last 2 messages."""
        try:
            amount = int(amount)
        except Exception:
            raise commands.BadArgument("Csak pozitív egész számú üzeneteket törölhetsz.")
        if amount <= 0:
            raise commands.BadArgument("Csak pozitív egész számú üzeneteket törölhetsz.")

        channel = ctx.message.channel
        amount = amount + 1  # the command counts as a message too, so if we'd like to del x, we should del x + 1
        if (amount > 5) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send("``Nice try Tici`` :upside_down:", delete_after=15)
        else:
            deleted = await channel.purge(limit=amount, bulk=True)
            await ctx.send(f"Deleted {len(deleted)} messages. :sparkles: :broom:", delete_after=5)

    @commands.command()
    async def csgomaps(self, ctx, amount: str = "1"):
        """Prints a given number of random CS:GO maps' name. Default is one map. Syntax: ?csgomaps number[int]"""
        try:
            amount = int(amount)
        except ValueError:
            raise commands.BadArgument("Csak pozitív egész számot adhatsz meg.")
        if amount <= 0:
            raise commands.BadArgument("Csak pozitív egész számot adhatsz meg.")
        maps = [
            "Dust 2",
            "Mirage",
            "Inferno",
            "Office",
            "Cache",
            "Nuke",
            "Train",
            "Vertigo",
            "Overpass",
            "Chlorine",
            "Anubis",
            "Agency"
        ]
        if amount <= 10:
            maps_str = random.choice(maps)  # the string that will be sent
            for x in range(0, amount - 1):
                maps_str += f"\n{random.choice(maps)}"
            await ctx.send(f"{maps_str}")
        else:
            raise commands.BadArgument("Maximum 10 pályát randomizálhatsz.")

    @commands.command(aliases=["srvinfo", "srvinf", "server", "srv", "guild", "serverinfo"])
    async def guildinfo(self, ctx):
        """Shows info about this Discord server"""
        guild = ctx.guild
        created_at = f"Server created: {guild.created_at}"
        guild_owner_about = f"**{guild.owner.name}** (currently **{guild.owner.status}**)"
        embed = discord.Embed(
            title=f"``{guild.name}:``",
            description=f"A Discord server with {guild.member_count} members",
            colour=discord.Colour.dark_purple()
        )
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        embed.set_author(name=f"Here you go, {ctx.author.display_name}!", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"This message was requested by {ctx.author.name}")
        embed.add_field(name="Admin:", value=f"{guild_owner_about}", inline=False)
        embed.add_field(name="Created at:", value=f"{created_at}", inline=False)
        embed.add_field(name="ServerID:", value=f"{guild.id}", inline=True)
        embed.add_field(name="Region:", value=f"{guild.region}", inline=True)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=["about", "user", "usr"])
    async def userinfo(self, ctx, member_id: int = None):
        """Shows info about a guild member. If no ID is passed, info about the message author will be shown."""
        now = datetime.datetime.now()
        # ha nem ad meg ID-t, akkor feltételezzük, hogy magáról akar infót
        member = ctx.author if not member_id else ctx.message.guild.get_member(member_id)  # fetches the member by id
        if not member:  # member might be None if he's offline or the user with the given id is not in this server
            await ctx.send(":x: A lekérdezett azonosítójú felhasználó nem elérhető. Lehet, hogy offline, vagy "
                           "hibás ID-t adtál meg.")
            return
        activity = member.activity.name if member.activity else member.activity
        if member.voice:
            user_voice_state = f"Currently connected to channel {member.voice.channel.name}"
        else:
            user_voice_state = f"{member.name} is currently not connected to any voice channels."

        embed = discord.Embed(
            title=f"``{member.name}:``",
            description=f"A Discord user since {member.created_at}",
            colour=discord.Colour.gold()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"Here you go, {ctx.author.display_name}!", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"This message was requested by {ctx.author.name} at {now}")
        embed.add_field(name="First appearance on this server:", value=f"{member.joined_at}", inline=False)
        embed.add_field(name="Top role on this server:", value=f"{member.top_role}", inline=False)
        embed.add_field(name="ID:", value=f"{member.id}", inline=True)
        embed.add_field(name="Bot:", value=f"{str(member.bot)}", inline=True)
        embed.add_field(name="Status:", value=f"{member.status}", inline=True)
        embed.add_field(name="Activity:", value=f"{activity}", inline=True)
        embed.add_field(name="VoiceState:", value=f"{user_voice_state}", inline=False)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=["testrole", "testRole", "test", "testing"])
    async def tester(self, ctx):
        """Grants permission to access the bot's test channel."""
        member = ctx.author
        await ctx.message.delete()
        role = discord.utils.get(member.guild.roles, name="tester")
        await member.add_roles(role)
        await ctx.send(f"Tester role assigned to {ctx.author.mention}")
        await ctx.message.delete()

    @commands.command(hidden=True)
    async def nsfw(self, ctx):
        member = ctx.message.author
        role_to_add = discord.utils.get(ctx.guild.roles, name="nsfw")
        minimum_role = discord.utils.get(ctx.guild.roles, name="Balaton Squad")
        top_role = member.top_role
        if minimum_role <= top_role:
            await member.add_roles(role_to_add)
            await ctx.message.delete()
            await self.bot.get_channel("logs").send(f"{member.name} has access to nsfw from now on.")
            await ctx.send(f"Hey {ctx.message.author.mention}, access granted!")
        else:
            await ctx.send("You don't have a high enough role to do that. :no_entry:")

    @commands.command(aliases=["cointoss", "headsortails", "érme", "coinflip", "pénzfeldobás"])
    async def coin(self, ctx):
        """Simulates a coin toss."""
        fejvagyiras = random.randint(0, 1)
        cointoss_array = ["fej", "írás"]
        await ctx.send(f"{cointoss_array[fejvagyiras]}")

    @commands.command()
    async def google(self, ctx):
        """Returns a Google search link."""
        szavak = ctx.message.content.split()
        meddig = len(szavak)
        link = f"https://www.google.com/search?q={szavak[1]}"
        for x in range(2, meddig):
            link += '+' + szavak[x]
        await ctx.send(f"{link}")

    @commands.command(aliases=["LMGTFY", "letmegoogle", "lmgoogle", "google2"])
    async def lmgtfy(self, ctx):
        """LMGTFY"""
        szavak = ctx.message.content.split()
        meddig = len(szavak)
        link = f"http://lmgtfy.com/?q={szavak[1]}"
        for x in range(2, meddig):
            link += '+' + szavak[x]
        await ctx.send(f"{link}")

    @commands.command(aliases=["LMGTFYIMG", "letmegoogleimg", "lmgoogleimg", "google3", "googleimg"])
    async def lmgtfyimg(self, ctx):
        """LMGTFY (images)"""
        szavak = ctx.message.content.split()
        meddig = len(szavak)
        link = f"http://lmgtfy.com/?t=i&q={szavak[1]}"
        for x in range(2, meddig):
            link += '+' + szavak[x]
        await ctx.send(f"{link}")

    @commands.command(aliases=["suggestion", "javaslat", "ötlet", "idea", "pleaseadd"])
    async def suggest(self, ctx):
        """Write your suggestions regarding the bot after '?suggest'."""
        file = open("/srv/shared/Simi/programozas/discordbot/0javaslatok.txt", "a")
        file.write("\n")
        file.write(f"{ctx.author}: {ctx.message.content},")
        file.close()
        message = ctx.message
        await message.add_reaction(u"\U0001F44C")
        await self.bot.get_channel("test").send(f"{ctx.guild.owner.mention} new suggestion(s)!")

    @commands.command(aliases=["plsfix", "pleasefix", "fix"])
    async def bug(self, ctx):
        """You can report bugs by typing '?bug' and the problem(s) you've encountered."""
        file = open("/srv/shared/Simi/programozas/discordbot/0bugs.txt", "a")
        file.write("\n")
        file.write(f"{ctx.author}: {ctx.message.content},")
        file.close()
        message = ctx.message
        await message.add_reaction(u"\U0001F916")
        await self.bot.get_channel("test").send(f"{ctx.guild.owner.mention} possible bug(s) reported!")

    @commands.command(aliases=["ut"])
    async def uptime(self, ctx):
        timedelta = datetime.datetime.now() - self.bot.online_since
        await ctx.message.delete()
        td_seconds = timedelta.total_seconds()
        td = {"days": int(td_seconds / 84600),
              "hours": int(td_seconds / 3600 % 24),
              "minutes": int(td_seconds / 60 % 60),
              "seconds": int(td_seconds % 60)}

        # strings in singular or plural form depending on the values they stand after
        hour = "hour" if td["hours"] == 1 else "hours"
        minute = "minute" if td["minutes"] == 1 else "minutes"
        second = "second" if td["seconds"] == 1 else "seconds"
        uptime = f"{td['hours']} {hour}, {td['minutes']} {minute} and {td['seconds']} {second}"

        if timedelta.days == 0:
            await ctx.send(f"``Uptime: {uptime}``")
        else:
            day = "day" if td["days"] == 1 else "days"
            await ctx.send(f"``Uptime: {td['days']} {day}, {uptime}``")


def setup(bot):
    bot.add_cog(Commands(bot))
