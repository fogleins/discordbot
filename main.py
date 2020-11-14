import datetime
import traceback
import gc

import click
import discord
from discord.ext import commands

from cogs.database import Database
from cogs.hardware import get_system_uptime


class SzeduletesBot(commands.Bot):
    # the extensions that need to be loaded from the cogs folder
    extensions = [
        "cogs.adminonly",
        "cogs.events",
        "cogs.base_commands",
        "cogs.commands",
        "cogs.balaton",
        "cogs.experimental",
        # "cogs.bmesch",
        "cogs.hardware"
    ]

    def __init__(self):
        super().__init__(command_prefix=".")
        self.online_since = datetime.datetime.now()
        self._channel_cache = dict()

        for ext in self.extensions:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f"{ext} cannot be loaded. [{e}]")
                traceback.print_exc()

    def run(self):
        """Starts the bot."""
        db = Database()
        token = db.query("SELECT token FROM tokens WHERE name = ?", ("ellbot",))[0]
        db.close()
        super().run(token)

    async def close(self):
        """Stops the bot."""
        await super().close()
        gc.collect()  # explicit garbage collector call

    def get_channel(self, channel_name):
        """
        Returns a discord.TextChannel object
        :param channel_name: The name of the channel
        :return: The TextChannel object with the given name
        :raise: ChannelNotFound if the channel name was not found in the database
        """
        if type(channel_name) is int:  # some funcions may call this method with a channel id
            return super().get_channel(channel_name)
        elif channel_name in self._channel_cache:
            channel_id = self._channel_cache[channel_name]
        else:
            db = Database()
            channel_id = db.query("SELECT id FROM text_channels WHERE name = ?", (channel_name,))[0]
            if channel_id is not None:
                self._channel_cache[channel_name] = channel_id
            else:
                raise commands.ChannelNotFound("Bad channel name argument.")
        return super().get_channel(channel_id)

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name="commands || ?help"))
        await self.get_channel("test").send(f"``[{datetime.datetime.now()}; System uptime: {get_system_uptime()}]`` "
                                            f"I'm back online! :globe_with_meridians: :white_check_mark:")
        print(f"Logged in as {self.user.name}\n{self.user.id}\n------\n")


@click.group(invoke_without_command=True, options_metavar='[options]')
@click.pass_context
def main(ctx):
    bot = SzeduletesBot()
    bot.run()


if __name__ == '__main__':
    main()
