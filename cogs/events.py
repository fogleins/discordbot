import datetime
import discord
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.datetime.now()
        role = discord.utils.get(member.guild.roles, name='newcomer')
        await member.add_roles(role)
        simiid = '<@358992693453652000>'
        uzenet = f"{member.name} ({member.id}) is now part of this discord server!"
        embed = discord.Embed(
            title=f'``{now}:`` ',
            description=f'{uzenet}',
            colour=discord.Colour.magenta()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name + ' has joined the server', icon_url=member.avatar_url)
        embed.add_field(name='Hey,', value=f"{simiid} you need to see this!")
        await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.datetime.now()
        simiid = '<@358992693453652000>'
        uzenet = f"{member.name} ({member.id}) is now part of this discord server!"
        embed = discord.Embed(
            title=f"``{now}:``",
            description=f"{uzenet}",
            colour=discord.Colour.dark_magenta()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name + " has joined the server", icon_url=member.avatar_url)
        embed.add_field(name='Hey,', value = f"{simiid} you need to see this!")
        await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if (before.id == after.id) and (after.id == 552216488803827713):
            if (str(before.status) == 'online') and (str(after.status) == 'offline'):
                await self.bot.get_channel(549709362206081076).send('Hey <@358992693453652000>, ' +
                    f' we need you! {after.name} is not under control!')
            elif (str(before.status) == 'offline') and (str(after.status) == 'online'):
                await self.bot.get_channel(549709362206081076).send("<@358992693453652000> I'm" +
                    " being watched. :eyes: ")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        now = datetime.datetime.now()
        if (after.author.bot is False) and (before.content != after.content):
            uzenet = (f"The message **{before.content}** has been edited to **{after.content}**" +
                f" by **{after.author.name}** in channel {after.channel.mention}")
            embed = discord.Embed(
                title=f"``{now}:`` ",
                description=f"{uzenet}",
                colour=discord.Colour.orange()
            )
            embed.set_thumbnail(url=after.author.avatar_url)
            embed.set_author(name=f'{after.author.name} has edited a message', icon_url=after.author.avatar_url)
            await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        now = datetime.datetime.now()
        kiirhato = False
        uzenet_content = message.content
        if (message.author.id == 549654750585421825 or uzenet_content.startswith('?')
            or uzenet_content.startswith('Unloaded') or uzenet_content.startswith('Loaded')
            or uzenet_content.startswith('User limit') or len(uzenet_content) > 1000
            or uzenet_content.startswith('\\') or uzenet_content.startswith('/////')):
                pass
        else:
            if message.attachments:
                try:
                    attachment_link = message.attachments[0].url
                    logba_ez_megy = (f"The following message was deleted from {message.channel.mention}:" +
                        f"{attachment_link}")
                    kiirhato = True
                except discord.DiscordException:
                    pass
                except IndexError:
                    pass
            else:
                logba_ez_megy = f'The message **{message.content}** was deleted from {message.channel.mention}'
                kiirhato = True
            embed = discord.Embed(
                title=f"``{now}:`` ",
                description=f"{logba_ez_megy}",
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_author(name=f"A message sent by {message.author.name} was deleted",
                icon_url=message.author.avatar_url)
            if kiirhato:
                await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        now = datetime.datetime.now()
        kiirhato = False
        if user.bot:
            pass
        else:
            if reaction.message.attachments:
                try:
                    # attachment_link = reaction.message.attachments[0]['url']
                    attachment_link = reaction.message.attachments[0].url
                    kiirando_uzenet = (f"{user.name} has added {reaction.emoji} to" 
                        f" {reaction.message.author}'s message in channel {reaction.message.channel.mention}"+
                        f" to the following message: {attachment_link}")
                    kiirhato = True
                except discord.DiscordException:
                    pass
                except IndexError:
                    pass
            else:
                kiirando_uzenet = (f"{user.name} has added {reaction.emoji} to {reaction.message.author}'s" +
                    f" message in channel {reaction.message.channel.mention} to the following message:" +
                    f" {reaction.message.content}")
                kiirhato = True
            embed = discord.Embed(
                title=f"``{now}:`` ",
                description=f"{kiirando_uzenet}",
                colour=discord.Colour.teal()
            )
            embed.set_thumbnail(url=reaction.message.author.avatar_url)
            embed.set_author(name=user.name + ' has added a reaction', icon_url=user.avatar_url)
            if kiirhato:
                await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        now = datetime.datetime.now()
        kiirhato = False
        if reaction.message.attachments:
            try:
                # attachment_link = reaction.message.attachments[0]['url']
                attachment_link = reaction.message.attachments[0].url
                kiirando_uzenet = (f"{user.name} has removed {reaction.emoji} from" +
                    f" {reaction.message.author}'s message in channel {reaction.message.channel.mention}" +
                    f" from the following message: {attachment_link}")
                kiirhato = True
            except discord.DiscordException:
                pass
            except IndexError:
                pass
        else:
            kiirando_uzenet = (f"{user.name} has removed {reaction.emoji} from {reaction.message.author}'s" +
                f" message in channel {reaction.message.channel.mention} from the following message:" +
                f" {reaction.message.content}")
            kiirhato = True
        embed = discord.Embed(
            title=f"``{now}:`` ",
            description=f"{kiirando_uzenet}",
            colour=discord.Colour.dark_teal()
        )
        embed.set_thumbnail(url=reaction.message.author.avatar_url)
        embed.set_author(name=user.name + ' has removed a reaction', icon_url=user.avatar_url)
        if kiirhato:
            await self.bot.get_channel(550724640469942285).send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            # ezt azért raktam ide, mert az id vizsgálatánál egyes esetekben errort ad
            # pl: on_voice_state_update error: 'NoneType' object has no attribute 'guild'
            if not member.bot:
                now = datetime.datetime.now()
                kiirhato = False
                nem_mute_az_event_oka = (bool((before.deaf == after.deaf)
                    and (before.mute == after.mute)
                    and (before.self_deaf == after.self_deaf)
                    and (before.self_mute == after.self_mute)
                    and (member.id != 549654750585421825)))
                if ((before.channel is None) and (after.channel.guild.id == 399595937409925140)
                    and (before.deaf == after.deaf) and (before.mute == after.mute)
                    and (before.self_deaf == after.self_deaf) and (before.self_mute == after.self_mute)
                    and (member.id != 549654750585421825)):
                        uzenet = f"**{member.name}** has just joined **{after.channel.name}**"
                        kiirhato = True
                elif ((before.channel.guild.id == 399595937409925140) and (after.channel is None)
                    and nem_mute_az_event_oka):
                        uzenet = f"**{member.name}** has disconnected from **{before.channel.name}**"
                        kiirhato = True
                elif ((before.channel.guild.id != 399595937409925140) and
                    (after.channel.guild.id == 399595937409925140) and nem_mute_az_event_oka):
                        uzenet = f"**{member.name}** has just joined **{after.channel.name}**"
                        kiirhato = True
                elif ((before.channel.guild.id == 399595937409925140)
                    and (after.channel.guild.id == 399595937409925140)
                    and (nem_mute_az_event_oka == True)):
                        uzenet = (f"**{member.name}** has moved from **{before.channel.name}** to" +
                            f" **{after.channel.name}**")
                        kiirhato = True
                if kiirhato:
                    embed = discord.Embed(
                        title=f"``{now}:`` ",
                        description=f"{uzenet}",
                        colour=discord.Colour.blue()
                    )
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_author(name=member.name + " has updated their VoiceState", icon_url=member.avatar_url)
                    await self.bot.get_channel(550724640469942285).send(embed=embed)
        except Exception as e:
            await self.bot.get_channel(550724640469942285).send(f"on_voice_state_update error: {e}")

    # does work
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        now = datetime.datetime.now()
        try:
            embed = discord.Embed(
                title=f"``{now}:`` ",
                description=f":interrobang: Command error: {error}",
                colour=discord.Colour.from_rgb(255, 0, 13)
            )
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.set_author(name='Command error', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/185/cross-mark_274c.png')
            await ctx.send(embed = embed)
        except Exception as e:
            print("Command error. I wasn't able to send an error message to the Discord channel in which" +
                f" I've encountered the error. ({e})")

def setup(bot):
    bot.add_cog(Events(bot))