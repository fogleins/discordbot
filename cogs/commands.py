import datetime
import random
import discord
from discord.ext import commands

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpme(self, ctx):
        'Basic info'
        await ctx.send("Development in progress. If you need help with commands, type '?help'," +
            " if you need further assistance, mention Simi (@Simi#4387)")

    @commands.command(aliases = ['hi', 'háló', 'halo'])
    async def hello(self, ctx):
        'Says world'
        await ctx.send('world')
        await ctx.message.delete()

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        'Adds two numbers together.'
        await ctx.send(left + right)

    @commands.command()
    async def changelog(self, ctx):
        "Prints what's new in this version"
        #await ctx.send(":tada: MOVED TO REWRITE (V1.0.1) :tada: \n-You can queue songs from now on!
        # \n-Added ?uptime\n-Added commands for Balaton Squad :beach:\n-Added '?suggest' so that I can 
        # process your suggestions from now on.\n-Added '?bug', thus you can report all the bugs. :bug: 
        # \n-Added music bot commands! :headphones: :sunglasses: \n-Added autorole function for new members
        # \n-Added cs and lol commands for 1337\n-Added '?bye'. Type '?bye' if you are about to disconnect 
        # from the voice channel you're currently in.\n-Added aliases for some commands
        # \n-Updated CS map list based on the recent updates\n-Bug fixes :hammer:
        # \n-Type '?tester' to gain access to the bot's test channel")
        await ctx.send(":tada: MOVED TO REWRITE (V1.1.1) :tada:" + 
            "\n-Added basic music bot features, type ``?p help`` for more info. Note: you can still" +
                " use the bots in #music-bot-commands." + 
            "\n-Added commands for Balaton Squad: You can now add the song you're currently listening to" + 
                " on Spotify to this year's playlist! :beach:" + 
            "\n-Added aliases for some commands" + 
            "\n-Updated CS map list based on the recent updates" + 
            "\n-You can now set the number of max users in the ``Itt-nem-zavar-a-Szédületes`` channel." + 
                " The number of max users will be set to unlimited in one hour." + 
            "\n-Some messages will be changed to ASCII emojis. This includes messages " +
                " that start with a backslash (``\\``), for example ``\\lenny`` or ``\\shrug``." + 
            "\n-Added the command ``?kóka``. I'd rather not say anything about that, see it for yourself" + 
                " :smirk: :upside_down:" + 
            "\n-Added ``?ping`` to get the bot's response time. Since the bot connects to a US server, the" +
                " value - under normal circumstances - should be around 150 ms." +
            "\n-Added shortcuts to get some songs' link faster while using Rythm or FredBoat." +
            "\n-Bug fixes :hammer:" + 
            "\n-Type '?tester' to gain access to the bot's test channel")
        await ctx.message.delete()

    #NEW: experimental.?bulkdel
    # @commands.command()
    # async def clear(self, ctx, amount=3):
    #     'Obsolete of ?bulkdel. Deletes a given number of messages. Default: last 2 messages.'
    #     channel = ctx.message.channel
    #     messages = []
    #     async for message in channel.history(limit=int(amount)):
    #         messages.append(message)
    #     await channel.delete_messages(messages)
    #     await ctx.send('Messages deleted. :ok_hand:')

    #bulk delete, hogy a ?clear ne triggerelje az on_message_delete eventet
    @commands.command(aliases=['delete', 'del', 'c', 'clear', 'purge'])
    # amount a törlendő üzenetek száma 
    # (3 a minimum, mert magát a commandot és legalább az utolsó 2 másik üzenetet töröljük)
    async def bulkdel(self, ctx, amount = 3): 
        """Updated version of ?clear. Deletes a given amount of messages, default is last 2 messages."""
        try:
            channel = ctx.message.channel
            if int(amount) >= 20:
                await ctx.send('``Nice try Tici`` :upside_down:', delete_after = 15)
            else:
                deleted = await channel.purge(limit = int(amount), bulk = True)
                await ctx.send(f"Deleted {len(deleted)} messages. :sparkles: ", delete_after = 5)
        except Exception as error:
            await ctx.send(f"Couldn't delete messages. ({error})")

    @commands.command()
    async def csgomap(self, ctx):
        """This is a legacy command. You can now use ?csgomaps without arguments to get one random map's name.
        Prints a random CS:GO map's name."""
        mapID = random.randint(0, 12)
        mapok = [
            'Dust 2',
            'Mirage', 
            'Inferno', 
            'Office', 
            'Cache', 
            'Nuke', 
            'Train', 
            'Vertigo (rip Cobblestone)', 
            'Overpass', 
            'Abbey', 
            'Zoo', 
            'Biome', 
            'Agency'
        ]
        await ctx.send('{}'.format(mapok[mapID]))

    @commands.command()
    async def csgomaps(self, ctx, amount = 1):
        "Prints a given number of random CS:GO maps' name. Default is one map. Syntax: ?csgomaps number[int]"
        #meddig = int(ctx.message.content[10:])
        meddig = int(amount)
        for x in range(0, meddig):
            mapID = random.randint(0, 12)
            mapok = [
                'Dust 2', 
                'Mirage', 
                'Inferno', 
                'Office', 
                'Cache', 
                'Nuke', 
                'Train', 
                'Vertigo (rip Cobblestone)', 
                'Overpass', 
                'Abbey', 
                'Zoo', 
                'Biome', 
                'Agency'
            ]
            await ctx.send('{}'.format(mapok[mapID]))

    @commands.command(aliases=['srvinfo', 'srvinf', 'server', 'srv', 'aboutserver', 'serverinfo'])
    async def guildinfo(self, ctx):
        'Shows info about this Discord server'
        guild = ctx.guild
        created_at = 'Server created: {}'.format(guild.created_at)
        member_count = '{}'.format(guild.member_count)
        name = guild.name
        region = guild.region
        srv_id = guild.id
        guild_owner_about = '**{}** (currently **{}**)'.format(guild.owner.name, guild.owner.status)
        embed = discord.Embed(
            title='``{}:`` '.format(name), 
            description='A Discord server with {} members'.format(member_count), 
            colour=discord.Colour.dark_purple()
        )
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        embed.set_author(name=f'Here you go, {ctx.author.display_name}!', icon_url=ctx.author.avatar_url)
        embed.set_footer(text='This message was requested by {}'.format(ctx.author.name))
        embed.add_field(name='Admin:', value='{}'.format(guild_owner_about), inline=False)
        embed.add_field(name='Created at:', value='{}'.format(created_at), inline=False)
        embed.add_field(name='ServerID:', value='{}'.format(srv_id), inline=True)
        embed.add_field(name='Region:', value='{}'.format(region), inline=True)
        await ctx.message.delete()
        await self.bot.get_channel(ctx.channel.id).send(embed=embed)

    @commands.command(aliases = ['userabout', 'aboutuser', 'usr'])
    async def userinfo(self, ctx):
        """Shows info about a guild member. If no ID is passed, info about the message author will be shown."""
        now = datetime.datetime.now()
        member = ctx.author
        #ha nem ad meg ID-t, akkor feltételezzük, hogy magáról akar infót
        if len(ctx.message.content.split()) == 1:
            usr_name = member.name
            usr_id = member.id
            usr_is_bot = str(member.bot)
            usr_avatar = member.avatar_url
            usr_acc_created = member.created_at
            usr_first_time_on_guild = member.joined_at
            usr_activity = member.activity
            usr_status = member.status
            usr_toprole = member.top_role
            if member.voice:
                usr_voicestate = "Currently connected to channel {}".format(member.voice.channel.name)
            else:
                usr_voicestate = "{} is currently not connected to any voice channels.".format(usr_name)
        else:
            guild = ctx.message.guild
            msg_content_split = ctx.message.content.split()
            usr_id = int(msg_content_split[1])
            member = guild.get_member(usr_id)
            usr_name = member.name
            usr_is_bot = str(member.bot)
            usr_avatar = member.avatar_url
            usr_acc_created = member.created_at
            usr_first_time_on_guild = member.joined_at
            usr_activity = str(member.activity)
            usr_status = member.status
            usr_toprole = member.top_role
            if member.voice:
                usr_voicestate = "Currently connected to channel {}".format(member.voice.channel.name)
            else:
                usr_voicestate = "{} is currently not connected to any voice channels.".format(usr_name)
            #user = discord.utils.get(ctx.message.guild.members, name=member.name)
            #member = discord.utils.get(message.guild.members, name='Foo')
        embed = discord.Embed(
            title='``{}:`` '.format(usr_name), 
            description='A Discord user since {}'.format(usr_acc_created), 
            colour=discord.Colour.gold()
        )
        embed.set_thumbnail(url=usr_avatar)
        embed.set_author(name=f'Here you go, {ctx.author.display_name}!', icon_url=ctx.author.avatar_url)
        embed.set_footer(text='This message was requested by {} at {}'.format(ctx.author.name, now))
        embed.add_field(name='First appearance on this server:', value='{}'.format(usr_first_time_on_guild), 
            inline=False)
        embed.add_field(name='Top role on this server:', value='{}'.format(usr_toprole), inline=False)
        embed.add_field(name='Bot:', value='{}'.format(usr_is_bot), inline=True)
        embed.add_field(name='Status:', value='{}'.format(usr_status), inline=True)
        embed.add_field(name='Activity:', value='{}'.format(usr_activity), inline=True)
        embed.add_field(name='VoiceState:', value='{}'.format(usr_voicestate), inline=False)
        await ctx.message.delete()
        await self.bot.get_channel(ctx.channel.id).send(embed=embed)


    @commands.command(aliases=['testrole', 'testRole', 'test'])
    async def tester(self, ctx):
        "Grants permission to access the bot's test channel."
        member = ctx.author
        await ctx.message.delete()
        role = discord.utils.get(member.guild.roles, name='tester')
        await member.add_roles(role)
        await ctx.send('Tester role assigned to {}'.format(ctx.author.mention))
        await ctx.message.delete()

    @commands.command(hidden = True)
    async def nsfw(self, ctx):
        member = ctx.message.author
        guild = ctx.message.guild
        role_to_add = discord.utils.get(ctx.guild.roles, name='nsfw')
        #role_to_add = guild.get_role(568123860281720845) #nsfw role id-je
        minimum_role1 = discord.utils.get(ctx.guild.roles, name='Balaton Squad')
        #minimum_role1 = guild.get_role(448507973741051904) #balaton squad role id-je
        #minimum_role2 = discord.utils.get(member.guild.roles, name='sub')
        top_role = member.top_role
        if minimum_role1 <= top_role:
            try:
                await member.add_roles(role_to_add)
                await ctx.message.delete()
                await self.bot.get_channel(549709362206081076).send('<@358992693453652000>' +
                    f' {member.name} has access to nsfw from now on.')
                await ctx.send("Hey {}, access granted!".format(ctx.message.author.mention))
            except Exception as error:
                await ctx.send("Something went wrong. :( ({})".format(error))
        else:
            await ctx.send("You don't have a high enough role to do that. :no_entry: ")

    @commands.command()
    async def update(self, ctx):
        'The bot sends this message before getting an update.'
        if ctx.author.id == 358992693453652000:
            msg = ":warning: I'll be offline for a few minutes. I'll be fresher when I come back. :warning:"
            await ctx.send(f'{msg}')
        else:
            await ctx.send("You don't have permissions to do that. :no_entry:")

    @commands.command(aliases = ['CS', 'CSGO', 'csgo', 'mm'])
    async def cs(self, ctx):
        'Asks the @1337 group if they want to play CS.'
        darab = ctx.message.content.split()
        darab_command_nelkul = darab[1:]
        kiirashoz = ' '.join(darab_command_nelkul)
        await ctx.message.delete()
        if len(darab) >= 2:
            await ctx.send('<@&444159433421881355> cs {} ?'.format(kiirashoz))
        else:
            await ctx.send('<@&444159433421881355> valaki cs?')

    @commands.command(aliases = ['LoL', 'Lol', 'liga'])
    async def lol(self, ctx):
        'Asks the @1337 group if they want to play LoL.'
        darab = ctx.message.content.split()
        darab_command_nelkul = darab[1:]
        kiirashoz = ' '.join(darab_command_nelkul)
        await ctx.message.delete()
        if len(darab) >= 2:
            await ctx.send('<@&444159433421881355> lol {} ?'.format(kiirashoz))
        else:
            await ctx.send('<@&444159433421881355> valaki lol?')

    @commands.command(aliases=['cointoss', 'headsortails', 'érme', 'coinflip', 'pénzfeldobás'])
    async def coin(self, ctx):
        'Simulates a coin toss.'
        fejvagyiras = random.randint(0, 1)
        cointoss_array = ['fej', 'írás']
        await ctx.send('{}'.format(cointoss_array[fejvagyiras]))

    @commands.command(aliases=['gn', 'goodnight', 'goodbye', 'szia'])
    async def bye(self, ctx):
        "This will send a goodbye message for you so you don't have to type that much."
        rnd_byeMsg = random.randint(1, 5)
        if rnd_byeMsg == 1:
            await ctx.send('{} is now leaving.:cry: Come back soon!'.format(ctx.author.mention))
        elif rnd_byeMsg == 2:
            await ctx.send(f'Our buddy {ctx.author.mention} is going to be offline for some time.' + 
                ' Say goodbye! :wave:')
        elif rnd_byeMsg == 3:
            await ctx.send('{} cannot stand us anymore. He is leaving now.'.format(ctx.author.mention))
        elif rnd_byeMsg == 4:
            await ctx.send('{} has something better to do. He is taking off.'.format(ctx.author.mention))
        else:
            await ctx.send(f'Unfortunately {ctx.author.mention} has got to go. What a shame!' +
                ' :smirk: :upside_down:')

    @commands.command()
    async def created(self, ctx):
        'Returns when a Discord ID was created.'
        try:
            vizsgalt_ID = int(ctx.message.content[9:26])
            letrehozva = discord.utils.snowflake_time(vizsgalt_ID)
            await ctx.send('{}'.format(letrehozva))
        except Exception as error:
            await ctx.send("Error. Did you enter a DiscordID? ({})".format(error))

    @commands.command()
    async def google(self, ctx):
        'Returns a Google search link.'
        szavak = ctx.message.content.split()
        meddig = len(szavak)
        link = 'https://www.google.com/search?q=' + szavak[1]
        for x in range(2, meddig):
            link += '+' + szavak[x]
        await ctx.send('{}'.format(link))

    @commands.command(aliases=['LMGTFY', 'letmegoogle', 'lmgoogle', 'google2'])
    async def lmgtfy(self, ctx):
        'LMGTFY'
        szavak = ctx.message.content.split()
        meddig = len(szavak)
        link = 'http://lmgtfy.com/?q=' + szavak[1]
        for x in range(2, meddig):
            link += '+' + szavak[x]
        await ctx.send('{}'.format(link))

    @commands.command(aliases=['LMGTFYIMG', 'letmegoogleimg', 'lmgoogleimg', 'google3', 'googleimg'])
    async def lmgtfyimg(self, ctx):
        'LMGTFY (images)'
        szavak = ctx.message.content.split()
        meddig = len(szavak)
        link = 'http://lmgtfy.com/?t=i&q=' + szavak[1]
        for x in range(2, meddig):
            link += '+' + szavak[x]
        await ctx.send('{}'.format(link))

    @commands.command(aliases=['suggestion', 'javaslat', 'ötlet', 'idea', 'pleaseadd'])
    async def suggest(self, ctx):
        "Write your suggestions regarding the bot after '?suggest'."
        file = open('/srv/shared/Simi/programozas/discordbot/0javaslatok.txt', 'a')
        file.write('\n')
        file.write('{}: {},'.format(ctx.author, ctx.message.content))
        file.close()
        message = ctx.message
        await message.add_reaction(u"\U0001F44C")
        await self.bot.get_channel(549709362206081076).send('<@358992693453652000> new suggestion(s)!')

    @commands.command(aliases=['bogár', 'hiba', 'bág', 'issue', 'plsfix', 'pleasefix', 'fix', 'bugos'])
    async def bug(self, ctx):
        "You can report bugs by typing '?bug' and the problem(s) you've encountered."
        file = open('/srv/shared/Simi/programozas/discordbot/0bugs.txt', 'a')
        file.write('\n')
        file.write('{}: {},'.format(ctx.author, ctx.message.content))
        file.close()
        message = ctx.message
        await message.add_reaction(u"\U0001F916")
        await self.bot.get_channel(549709362206081076).send('<@358992693453652000> possible bug(s) reported!')

def setup(bot):
    bot.add_cog(Commands(bot))