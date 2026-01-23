import sqlite3


def open_connection():
    global connect, cursor
    connect = sqlite3.connect("match_autopsy.db")
    cursor = connect.cursor()


def close_connection():
    connect.close()


def init_db():
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS accounts (
        puuid TEXT PRIMARY KEY,
        riot_id TEXT,
        tag_line TEXT
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS matches (
        match_id TEXT PRIMARY KEY,
        puuid TEXT NOT NULL,
        match_date LONG,
        game_duration INTEGER,
        champion_name TEXT,
        assists INTEGER,
        deaths INTEGER,
        gold_earned INTEGER,
        kills INTEGER,
        vision_score INTEGER,
        role TEXT,
        lane_minions_killed INTEGER,
        jungle_minions_killed INTEGER,
        kill_participation FLOAT,
        game_cs_per_minute FLOAT,
        total_damage_dealt_to_champions INTEGER,
        win BOOLEAN,
        gold_at_10 INTEGER,
        cs_at_10 INTEGER,
        xp_at_10 INTEGER,
        gold_diff_at_15 INTEGER,
        FOREIGN KEY (puuid) REFERENCES accounts(puuid)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS events (
        match_id TEXT NOT NULL,
        puuid TEXT NOT NULL,
        participant_id INTEGER NOT NULL,
        timestamp INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        FOREIGN KEY (match_id) REFERENCES matches(match_id),
        FOREIGN KEY (puuid) REFERENCES accounts(puuid)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS features (
        match_id TEXT NOT NULL,
        puuid TEXT NOT NULL,
        feature_name TEXT NOT NULL,
        feature_value FLOAT NOT NULL,
        FOREIGN KEY (match_id) REFERENCES matches(match_id),
        FOREIGN KEY (puuid) REFERENCES accounts(puuid)
    )
    """
    )

    connect.commit()


def account_exists(puuid: str) -> bool:
    cursor.execute("SELECT 1 FROM accounts WHERE puuid = ?", (puuid,))
    return cursor.fetchone() is not None


def insert_account(puuid: str, gameName: str, tagLine: str):
    cursor.execute(
        "INSERT INTO accounts (puuid, riot_id, tag_line) VALUES (?, ?, ?)",
        (puuid, gameName, tagLine),
    )
    connect.commit()


def insert_match(match: dict):
    cursor.execute(
        "INSERT INTO matches (match_id, puuid, match_date, game_duration, champion_name, assists, deaths, gold_earned, kills, vision_score, role, lane_minions_killed, jungle_minions_killed, kill_participation, game_cs_per_minute, total_damage_dealt_to_champions, win, gold_at_10, cs_at_10, xp_at_10, gold_diff_at_15) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            match["match_id"],
            match["puuid"],
            match["match_date"],
            match["game_duration"],
            match["champion_name"],
            match["assists"],
            match["deaths"],
            match["gold_earned"],
            match["kills"],
            match["vision_score"],
            match["role"],
            match["lane_minions_killed"],
            match["jungle_minions_killed"],
            match["kill_participation"],
            match["game_cs_per_minute"],
            match["total_damage_dealt_to_champions"],
            match["win"],
            match["gold_at_10"],
            match["cs_at_10"],
            match["xp_at_10"],
            match["gold_diff_at_15"],
        ),
    )
    connect.commit()


def insert_event(event: dict):
    cursor.execute(
        "INSERT INTO events (match_id, puuid, timestamp, event_type, participant_id) VALUES (?, ?, ?, ?, ?)",
        (
            event["match_id"],
            event["puuid"],
            event["timestamp"],
            event["event_type"],
            event["participant_id"],
        ),
    )


def get_existing_match_ids(puuid: str) -> set:
    cursor.execute("SELECT match_id FROM matches WHERE puuid = ?", (puuid,))
    rows = cursor.fetchall()
    return {row[0] for row in rows}


def get_match_ids_by_puuid(puuid: str) -> list[str]:
    cursor.execute(
        "SELECT match_id FROM matches WHERE puuid = ? ORDER BY match_date DESC",
        (puuid,),
    )
    rows = cursor.fetchall()
    return [row[0] for row in rows]


def get_match(match_id: str, puuid: str) -> dict:
    cursor.execute(
        "SELECT * FROM matches WHERE match_id = ? AND puuid = ?", (match_id, puuid)
    )
    row = cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))


def get_events(match_id: str, puuid: str) -> list[dict]:
    cursor.execute(
        "SELECT * FROM events WHERE match_id = ? AND puuid = ?", (match_id, puuid)
    )
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def get_puuid_by_match_id(
    match_id: str,
) -> str:  # if i have two puuds for one match id this breaks
    cursor.execute("SELECT puuid FROM matches WHERE match_id = ?", (match_id,))
    row = cursor.fetchone()
    return row[0] if row else None


def features_exist(match_id: str, puuid: str) -> bool:
    cursor.execute(
        "SELECT 1 FROM features WHERE match_id = ? AND puuid = ?", (match_id, puuid)
    )
    return cursor.fetchone() is not None


def insert_feature(feature: dict):
    cursor.execute(
        "INSERT INTO features (match_id, puuid, feature_name, feature_value) VALUES (?, ?, ?, ?)",
        (
            feature["match_id"],
            feature["puuid"],
            feature["feature_name"],
            feature["feature_value"],
        ),
    )


def get_features(match_id: str, puuid: str) -> list[dict]:
    cursor.execute(
        "SELECT * FROM features WHERE match_id = ? AND puuid = ?", (match_id, puuid)
    )
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
