import discord
from discord.ext import commands
from subprocess import Popen, PIPE


class Hardware(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hdd(self, ctx):
        """Prints the HDD's status using HDSentinel"""
        try:
            j = ""  # Linux pw goes here
            p = ""  # Full path of the program that needs to be run goes here
            process = Popen([f"echo {j} | sudo -S {p}"], stdout=PIPE, shell=True)
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

                await ctx.send(f"```{hds_credits}\n{hds_startupmessage}\n{output}\n\nProgram returned {exit_code}```")
            else:
                await ctx.send(f"Valami :poop:\n{err.decode()}\nExit code: {exit_code}")
        except Exception as err:
            print(err)


def setup(bot):
    bot.add_cog(Hardware(bot))
