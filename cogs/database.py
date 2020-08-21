import sqlite3


def get_spotify_link(year: int):
    """
    Reads and returns a given year's playlist link from an SQLite database
    :param year: The year of which playlist's link will be returned
    :returns The link of the given year's playlist
    """
    try:
        db = sqlite3.connect("/srv/shared/Simi/programozas/discordbot/rwLive/resources/spotify.db")
        c = db.cursor()
        link = c.execute(f"SELECT link FROM spotify WHERE year={year}").fetchone()
        db.close()
        return link
    except sqlite3.OperationalError as e:
        raise RuntimeError(f"Hiba a link visszaadása során: {e}")
    except TypeError:
        raise RuntimeError("A megadott évi lista nem szerepel az adatbázisban.")


def update_last_in_voice(discord_id: int):
    """
    Updates a member's last seen time
    :param discord_id: The Discord id of the member who joined voice
    :return:
    """
    # if a member whose discordID is not in the database joins a voice channel, SQLite will not modify the database
    try:
        db = sqlite3.connect("/srv/shared/Simi/programozas/discordbot/rwLive/resources/members.db")
        c = db.cursor()
        # updating the 'lastInVoice' column in the database by inserting the current unix timestamp
        c.execute(f"UPDATE members SET lastInVoice = STRFTIME('%s', 'now', 'localtime') WHERE discordID = {discord_id}")
        db.commit()
        db.close()
    except sqlite3.OperationalError as e:
        raise RuntimeError(f"Hiba a belépés idejének frissítése során: {e}")
    except Exception as e:
        raise RuntimeWarning(f"Hiba a legutóbbi belépés idejének mentése során. ({e})")


def calculate_time_spent_in_voice(discord_id: int):
    """
    Calculates how much time a member has spent in voice
    :param discord_id: The Discord id of the member who disconnected
    :return: The time spent in voice, a datetime.datetime object
    """
    try:
        db = sqlite3.connect("/srv/shared/Simi/programozas/discordbot/rwLive/resources/members.db")
        c = db.cursor()
        c.execute(f"UPDATE members SET inVoiceDuration = (SELECT TIME(strftime('%s', 'now', 'localtime') - lastInVoice,"
                  f" 'unixepoch')) WHERE discordID = {discord_id}")
        timedelta = c.execute(f"SELECT inVoiceDuration FROM members WHERE discordID = {discord_id}").fetchone()[0]
        db.commit()
        db.close()
        return timedelta
    except sqlite3.OperationalError as e:
        raise RuntimeError(f"Hiba az online töltött idő kiszámítása során: {e}")
    except Exception as e:
        raise RuntimeWarning(f"Hiba a voice-ban töltött idő kiszámítása során. ({e})")
