import sqlite3


class Database:
    def __init__(self, path="../resources/discord.db"):
        self.path = path
        self.db = sqlite3.connect(path)  # the sqlite3 database object

    def open_db(self):
        """
        Opens the database and returns its cursor
        :return: An SQLite cursor object, the cursor of the database
        """
        self.db = sqlite3.connect(self.path)
        return self.db.cursor()

    def get_spotify_link(self, year: int):
        """
        Reads and returns a given year's playlist link from an SQLite database
        :param year: The year of which playlist's link will be returned
        :returns The link of the given year's playlist
        """
        try:
            c = self.open_db()
            year = (str(year),)  # this is the secure way, see https://docs.python.org/3/library/sqlite3.html
            link = c.execute("SELECT link FROM spotify WHERE year = ?", year).fetchone()
            if link is None:
                raise RuntimeError("A kért link nem létezik.")
            return link[0]
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Hiba a link visszaadása során: {e}")
        finally:
            self.db.close()

    def update_last_in_voice(self, discord_id: int):
        """
        Updates a member's last seen time
        :param discord_id: The Discord id of the member who joined voice
        :return:
        """
        # if a member whose discordID is not in the database joins a voice channel, SQLite will not modify the database
        try:
            c = self.open_db()
            # updating the 'lastInVoice' column in the database by inserting the current unix timestamp
            discord_id = (str(discord_id),)
            c.execute("UPDATE members SET lastInVoice = STRFTIME('%s', 'now', 'localtime') WHERE discordID = ?",
                      discord_id)
            self.db.commit()
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Hiba a belépés idejének frissítése során: {e}")
        finally:
            self.db.close()

    def calculate_time_spent_in_voice(self, discord_id: int):
        """
        Calculates how much time a member has spent in voice
        :param discord_id: The Discord id of the member who disconnected
        :return: The time spent in voice
        """
        try:
            c = self.open_db()
            discord_id = (str(discord_id),)
            c.execute("UPDATE members SET inVoiceDuration = (SELECT TIME(strftime('%s', 'now', 'localtime') "
                      "- lastInVoice, 'unixepoch')) WHERE discordID = ?", discord_id)
            timedelta = c.execute("SELECT inVoiceDuration FROM members WHERE discordID = ?", discord_id).fetchone()[0]
            self.db.commit()
            return timedelta
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Hiba az online töltött idő kiszámítása során: {e}")
        finally:
            self.db.close()

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
            c = self.open_db()
            # the member's last stored birthday date, e.g. if one has joined on their birthday in 2018, then the year
            # 2018 would be stored in the column 'lastDiscordBirthday', so if he/she invokes another voice_state_update
            # event, the birthday easter egg message would not be sent
            params = (str(discord_id), f"{month:02d}-{day:02d}")
            last_discord_bday = c.execute("SELECT lastDiscordBirthday FROM members WHERE (discordID = ? "
                                          "AND STRFTIME('%m-%d', DATE(birthday)) = ?)", params).fetchone()

            # checking whether the member has already gotten a birthday message
            if last_discord_bday is not None:
                bday_year = last_discord_bday[0]
                if bday_year == year:
                    return False  # a birthday message was already sent
                else:
                    # updating the year
                    params = (year, str(discord_id))
                    c.execute("UPDATE members SET lastDiscordBirthday = ? WHERE discordID = ?", params)
                    self.db.commit()
                    return True
            return False
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Adatbázishiba a születésnap meghatározása során: {e}")
        finally:
            self.db.close()

    def get_debt(self, discord_id: int):
        """
        :param discord_id: The discord ID of the member whose debt is returned
        :return: The amount the member owes :)
        """
        try:
            c = self.open_db()
            discord_id = (str(discord_id),)
            result = c.execute("SELECT fizetendo FROM siofok2020_fizetendo WHERE discordID = ?", discord_id).fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Adatbázishiba: {e}")
        finally:
            self.db.close()
