import datetime
import discord
from discord.ext import commands

from cogs.database import *


class BalatonSquad(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["balatonrole", "siofok", "siófok", "Siófok"])
    async def balaton(self, ctx):
        """Hozzáférést kaphatsz a 'balaton' channelhez."""
        member = ctx.author
        guild = ctx.message.guild
        role_to_add = discord.utils.get(member.guild.roles, name="Balaton Squad")
        must_have_role = discord.utils.get(member.guild.roles, name="newcomer")
        assigned_roles = ctx.author.roles
        if must_have_role in assigned_roles:
            await member.add_roles(role_to_add)
            await ctx.message.delete()
            await self.bot.get_channel("test").send(f"<@358992693453652000> {member.name} "
                                                    "is now part of Balaton Squad!")
            await ctx.send(f"Hey, {ctx.message.author.mention} you're part of Balaton Squad from now on!")
        else:
            await ctx.send(f"You don't have permission to be a member of Balaton Squad. "
                           f"Contact {guild.owner.name} if you want to gain access.")

    @commands.command(aliases=["zenejavaslat", "muzsika"])
    async def zene(self, ctx):
        """Idei siófoki playlistre kerülnek a '?zene' után írt zenék."""
        file = open("/srv/shared/Simi/programozas/discordbot/0zene.txt", "a")
        file.write("\n")
        file.write(f"{ctx.author}: {ctx.message.content}")
        file.close()
        message = ctx.message
        await message.add_reaction(u"\U0001F3A7")
        await self.bot.get_channel("test").send("<@358992693453652000> we've got new music "
                                                "to add to our playlist!")

    @commands.command(aliases=["spotify", "Spotify"])
    async def spotifyadd(self, ctx):
        """Ezt a parancsot használva az általad jelenleg hallgatott Spotify számot adhatod az idei siófoki playlisthez.
         Csak akkor működik, ha a Spotifyod össze van kötve a Discord fiókoddal."""
        member = ctx.message.author
        if member.activity:
            if member.activity.name == "Spotify":
                now = datetime.datetime.now()
                spotify = member.activity
                file = open("/srv/shared/Simi/programozas/discordbot/0zene.txt", "a")
                file.write("\n")
                file.write(f"{ctx.author}: {spotify.artist} - {spotify.title}, {spotify.duration} "
                           f"ID: spotify:track:{spotify.track_id}")
                file.close()
                message = ctx.message
                emoji = await ctx.message.guild.fetch_emoji(568431664519446547)
                await message.add_reaction(emoji)
                # visszajelzés
                author = f"{message.author.name} has suggested a song to add"
                uzenet = (f"**{ctx.author.name}** has added **{spotify.title}** by **{spotify.artist}** to "
                          "this year's Siófok playlist")
                embed2 = discord.Embed(
                    title=" ",
                    description=f"<:spotify:568431664519446547> {uzenet}",
                    colour=discord.Colour.green()
                )
                embed2.set_thumbnail(url=spotify.album_cover_url)
                embed2.set_author(name=f"{author}", icon_url=member.avatar_url)
                await ctx.send(embed=embed2)
                # log + simi
                await self.bot.get_channel("test").send("<@358992693453652000> we've got "
                                                                    "new music to add to our playlist!")
                uzenet = (f"**{ctx.author.name}** has added **{spotify.title}** by **{spotify.artist}** "
                          f"to this year's Siófok playlist")
                embed = discord.Embed(
                    title=f"``{now}:``",
                    description=f"{uzenet}",
                    colour=discord.Colour.green()
                )
                embed.set_thumbnail(url=spotify.album_cover_url)
                embed.set_author(
                    name=f"{ctx.author.name} has added {spotify.title} to the playlist",
                    icon_url=member.avatar_url
                )
                await self.bot.get_channel("logs").send(embed=embed)
            else:
                await ctx.send("No Spotify listening activity detected.")
        else:
            await ctx.send("No Spotify listening activity detected.")

    @commands.command(aliases=["link", "playlistre", "playlist"])
    async def zenelink(self, ctx, year: int = datetime.datetime.now().year):
        """
        Reads and returns a given year's playlist link from an SQLite database
        :param ctx: Context, gets passed automatically
        :param year: The year of which playlist's link will be returned
        :returns The link of the given year's playlist
        """
        db = None
        try:
            db = Database()
            link = db.query("SELECT link FROM spotify WHERE year = ?", (str(year),))
            if link is None:
                raise QueryReturnedNoneTypeError("A megadott év listája nem létezik.")
            await ctx.send(f"A {year} évi playlist linkje: {link[0]}")
        except sqlite3.DatabaseError:
            raise
        finally:
            if db is not None:
                db.close()

    @commands.command(aliases=["fizetendő"], hidden=True)
    async def fizetendo(self, ctx):
        """
        Visszaadja DiscordID alapján, hogy kinek-mennyi tartozása maradt
        :param ctx: The contex in which the command was invoked, its passed automatically by discord.py
        :return: The debt of the member who invoked the command
        """
        db = None
        try:
            db = Database()
            debt = db.query("SELECT fizetendo FROM siofok2020_fizetendo WHERE discordID = ?", (str(ctx.author.id),))
            await ctx.message.delete()
            await ctx.send(f"{debt[0]} Ft :money_with_wings:", delete_after=10)
        except sqlite3.DatabaseError as e:
            await ctx.send(f"Hiba: {e}")
        finally:
            if db is not None:
                db.close()


def setup(bot):
    bot.add_cog(BalatonSquad(bot))
