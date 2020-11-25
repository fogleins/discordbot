import sqlite3


# custom exception classes for handling database-related errors
class DatabaseError(Exception):
    pass


class QueryReturnedNoneTypeError(Exception):
    pass


class Database:
    # def __init__(self, path="../resources/data/discord.db"):
    def __init__(self, path="./resources/data/discord.db"):
        self._db = sqlite3.connect(path)
        self._cursor = self._db.cursor()

    def close(self):
        self._db.close()

    def commit(self):
        self._db.commit()

    def query(self, command, args):
        """
        Performs a SQLite query
        :param command: The SQLite query command
        :param args: An optional string containing a tuple of values included in the command: ("your_parameter",)
        :return: The result of the query, None if nothing was found. Only the first result is returned.
        """
        result = self._cursor.execute(command, args)
        if result is not None:
            return result.fetchone()
        return result

    def update_last_in_voice(self, discord_id: int):
        """
        Updates a member's last seen time
        :param discord_id: The Discord id of the member who joined voice
        :return:
        """
        # if a member whose discordID is not in the database joins a voice channel, SQLite will not modify the database
        try:
            # updating the 'lastInVoice' column in the database by inserting the current unix timestamp
            self.query("UPDATE members SET lastInVoice = STRFTIME('%s', 'now', 'localtime') WHERE discordID = ?",
                       (str(discord_id),))
            self.commit()
        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Hiba a belépés idejének frissítése során: {e}")

    def calculate_time_spent_in_voice(self, discord_id: int):
        """
        Calculates how much time a member has spent in voice
        :param discord_id: The Discord id of the member who disconnected
        :return: The time spent in voice
        """
        try:
            self.query("UPDATE members SET inVoiceDuration = (SELECT TIME(strftime('%s', 'now', 'localtime') "
                       "- lastInVoice, 'unixepoch')) WHERE discordID = ?", (str(discord_id),))
            self.commit()
            timedelta = self.query("SELECT inVoiceDuration FROM members WHERE discordID = ?", (str(discord_id),))
            if timedelta:
                return timedelta[0]
            return -1  # if the member was not in the database, we wont print the time spent in voice
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Hiba az online töltött idő kiszámítása során: {e}")

    def check_birthday(self, discord_id: int, year, month, day):
        """
        Checks whether a member who joined a voice channel has birthday today
        :param discord_id: The Discord ID of the member who joined the voice channel
        :param year: The current year
        :param month: The current month
        :param day: The current day of month
        :return: True, if the member's birthday is today and a birthday wish hasn't been sent yet
        """
        try:
            # the member's last stored birthday date, e.g. if one has joined on their birthday in 2018, then the year
            # 2018 would be stored in the column 'lastDiscordBirthday', so if he/she invokes another voice_state_update
            # event, the birthday easter egg message would not be sent
            params = (str(discord_id), f"{month:02d}-{day:02d}")
            last_discord_bday = self.query("SELECT lastDiscordBirthday FROM members WHERE (discordID = ? "
                                           "AND STRFTIME('%m-%d', DATE(birthday)) = ?)", params)

            # checking whether the member has already gotten a birthday message
            if last_discord_bday is not None:
                bday_year = last_discord_bday[0]
                if bday_year == year:
                    return False  # a birthday message was already sent
                else:
                    # updating the year
                    params = (year, str(discord_id))
                    self.query("UPDATE members SET lastDiscordBirthday = ? WHERE discordID = ?", params)
                    self.commit()
                    return True
            return False
        except sqlite3.DatabaseError as e:
            raise DatabaseError(f"Adatbázishiba a születésnap meghatározása során: {e}")

    def channel_is_reserved(self, channel_id):
        """
        Checks if the given channel is reserved (see the changelimit command)
        :param channel_id: The id of the channel
        :return: True if the channel is reserved and therefore can't be reserved now
        """
        try:
            channel_id = (str(channel_id),)
            result = self.query("SELECT isReserved FROM reservations WHERE channelID = ?", channel_id)
            return result is not None
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Adatbázishiba: {e}")
