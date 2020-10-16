import discord


class GuildVoiceChannel:
    def __init__(self, channel: discord.VoiceChannel):
        self.channel = channel
        self.is_reserved = channel.user_limit != 0

    async def set_user_limit(self, limit):
        """
        Reserves the given voice channel
        :param limit: The number of max users allowed to connect to the channel, 0 to set it to unlimited
        :return:
        """
        try:
            limit = int(limit)
            if limit < 0 or limit > 99:
                raise RuntimeError("Limit must be between 1 and 99.")
            await self.channel.edit(user_limit=limit)
            self.is_reserved = limit != 0
        except ValueError as e:
            raise RuntimeError(f"Hibás limit paraméter: {e}")

    def is_reserved(self):
        """
        Updates and returns the value of the is_reserved variable
        :return: True if the channel's limit is not 0
        """
        self.is_reserved = self.channel.user_limit != 0
        return self.is_reserved
