from discord.ext import commands
from subprocess import Popen, PIPE


class Hardware(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def rbp(self, ctx):  # rbp = raspberry pi
        await ctx.send("This is a command group, which currently has a single subcommand: ``hdd``. "
                       "Syntax: ``?rbp hdd``")

    @rbp.command()
    async def hdd(self, ctx):
        """Prints the HDD's status using HDSentinel"""
        await ctx.message.delete()
        # running the program as sudo is now handled using a shell script
        # for further information, read the following forum thread:
        # https://askubuntu.com/questions/155791/how-do-i-sudo-a-command-in-a-script-without-being-asked-for-a-password
        process = Popen(["sudo /srv/shared/Simi/programozas/discordbot/hdsentinel.sh"], stdout=PIPE, shell=True)
        (output, err) = process.communicate()
        exit_code = process.wait()

        if err is None:
            output = output.decode()    # Converts bytes to str
            output = output.split("\n\n")
            hds_credits = output[0]     # HDS Version...
            hds_startupmessage = output[1]  # Examining...
            output = output[2].split("\n")
            output.pop(2)   # removes the hdd's serial number from the output
            output = "\n".join(output)

            await ctx.send(f"```{hds_credits}\n\n{hds_startupmessage}\n{output}\n\nProgram returned {exit_code}```")
        else:
            await ctx.send(f"Valami :poop:\n{err.decode()}\nExit code: {exit_code}")

    @rbp.command()
    async def neofetch(self, ctx):
        """Gets the neofetch message and sends it to the Discord channel it was requested in"""
        await ctx.message.delete()
        # Both screenfetch and neofetch return highly formatted results, which do not appear in Discord correctly,
        # therefore this command is implemented for testing purposes only.
        process = Popen(["neofetch"], stdout=PIPE, shell=True)
        (output, err) = process.communicate()
        exit_code = process.wait()

        if err is None:
            output = output.decode()
            await ctx.send(f"```{output}\nProgram returned {exit_code}```")
        else:
            await ctx.send(f"Error: {err.decode()}")


def setup(bot):
    bot.add_cog(Hardware(bot))
