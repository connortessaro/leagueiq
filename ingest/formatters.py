from typing import Counter
import storage.db as db


def get_participant_id(match: dict, puuid: str) -> str | None:
    participants = match["info"]["participants"]
    
    for p in participants:
        if p["puuid"] == puuid:
            return str(p["participantId"])
    return None 


def format_match_events(timeline: dict, participant_id: int, puuid: str) -> list[dict]:

    events_list = []
    for frame in timeline["info"]["frames"]:
        events = frame["events"] 
        for event in events:    
            event_type = None
            if event["type"] == "CHAMPION_KILL":
                if event["timestamp"] < 600000 and event["victimId"] == participant_id:
                    event_type = "EARLY_DEATH"
            elif event["type"] == "BUILDING_KILL":
                if event["killerId"] == participant_id or participant_id in event.get("assistingParticipantIds", []):
                    event_type = "STRUCTURE_PARTICIPATION"
            elif event["type"] == "ELITE_MONSTER_KILL":
                if event["killerId"] == participant_id or participant_id in event.get("assistingParticipantIds", []):
                    if event["monsterType"] == "DRAGON":
                        event_type = "DRAGON_PARTICIPATION"
                    if event["monsterType"] == "BARON_NASHOR":
                        event_type = "BARON_PARTICIPATION"
                    if event["monsterType"] == "RIFT_HERALD":
                        event_type = "RIFT_HERALD_PARTICIPATION"

            if event_type is None:
                continue
            print(f"formatted event: {event_type} at {event['timestamp']} for participant {participant_id}")
            events_list.append(
                {
                    "match_id": timeline["metadata"]["matchId"],
                    "timestamp": event["timestamp"],
                    "event_type": event_type,
                    "participant_id": participant_id,
                    "puuid": puuid
                }
            )
    return events_list


def extract_timeline_checkpoints(timeline: dict, match: dict, puuid: str) -> dict:
    participant_id = get_participant_id(match, puuid)
    ten_min_frame = None
    fifteen_min_frame = None
    user = None
    opp_fifteen_min_frame = None

    for p in match["info"]["participants"]:
        if p["puuid"] == puuid:
            user = p
            break
    if user is None:
        return None

    user_position = user["teamPosition"]
    user_teamId = user["teamId"]

    opponent = None

    for p in match["info"]["participants"]:
        if p["teamId"] != user_teamId and p["teamPosition"] == user_position:
            opponent = p
            break

    opponent_participant_id = str(opponent["participantId"])

    for frame in timeline["info"]["frames"]:
        timestamp = frame["timestamp"]
        participant_frames = frame["participantFrames"]
        if timestamp >= 590000 and timestamp <= 610000:
            ten_min_frame = participant_frames[participant_id]

        if timestamp >= 89000 and timestamp <= 910000:
            fifteen_min_frame = participant_frames[participant_id]
            opp_fifteen_min_frame = participant_frames[opponent_participant_id]

    if ten_min_frame is None or fifteen_min_frame is None or opp_fifteen_min_frame is None:
        return None

    cs_at_10 = ten_min_frame["minionsKilled"] + ten_min_frame["jungleMinionsKilled"]
    gold_at_10 = ten_min_frame["totalGold"]
    xp_at_10 = ten_min_frame["xp"]
    gold_at_15 = fifteen_min_frame["totalGold"]
    oppo_gold_at_15 = opp_fifteen_min_frame["totalGold"]

    gold_diff_at_15 = gold_at_15 - oppo_gold_at_15 # positive means player is ahead

    checkpoints = {
        "cs_at_10": cs_at_10,
        "gold_at_10": gold_at_10,
        "xp_at_10": xp_at_10,
        "gold_diff_at_15": gold_diff_at_15,
    }
    return checkpoints


def new_matches(fetched_match_ids: list[str], puuid: str) -> list[str]:
    stored_matches = db.get_existing_match_ids(puuid)
    new_match_ids = [
        match_id for match_id in fetched_match_ids if match_id not in stored_matches
    ]

    return new_match_ids


def format_match(match: dict, puuid: str) -> dict:
    player = None  # player dict
    team = None  # team dict
    participants = match["info"]["participants"]
    for p in participants:
        if p["puuid"] == puuid:
            player = p
            for t in match["info"]["teams"]:
                if t["teamId"] == player["teamId"]:
                    team = t
                    break
            break

    jungle_cs = (
        player["totalAllyJungleMinionsKilled"]
        + player["totalEnemyJungleMinionsKilled"]
    )

    formatted_match = {
        "match_id": match["metadata"]["matchId"],
        "puuid": puuid,
        "match_date": match["info"]["gameCreation"],
        "game_duration": match["info"]["gameDuration"],
        "champion_name": player["championName"],
        "assists": player["assists"],
        "deaths": player["deaths"],
        "gold_earned": player["goldEarned"],
        "kills": player["kills"],
        "vision_score": player["visionScore"],
        "role": player["role"],
        "lane_minions_killed": player["totalMinionsKilled"],
        "jungle_minions_killed": jungle_cs,
        "kill_participation": player['challenges']["killParticipation"],
        "game_cs_per_minute": round(
            (player["totalMinionsKilled"] + jungle_cs)
            / (match["info"]["gameDuration"] / 60),
            2,
        ),
        "total_damage_dealt_to_champions": player["totalDamageDealtToChampions"],
        "win": team["win"],
    }
    return formatted_match
