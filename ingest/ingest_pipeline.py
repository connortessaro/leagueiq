from ingest.riot_client import (
    fetch_puuid,
    fetch_match_ids,
    fetch_match,
    fetch_match_timeline,
)
from ingest.formatters import (
    format_match,
    extract_timeline_checkpoints,
    get_participant_id,
    format_match_events,
    new_matches,
)
import storage.db as db


def ingest_account(game_name: str, tag_line: str) -> str:
    puuid = fetch_puuid(game_name, tag_line)
    if not db.account_exists(puuid):
        db.insert_account(puuid, game_name, tag_line)
    return puuid


def ingest_matches(puuid: str, count: int) -> list[int]:
    fetched_match_ids = fetch_match_ids(puuid, count)

    # Determine which matches are new
    match_ids_to_ingest = new_matches(fetched_match_ids, puuid)

    for match_id in match_ids_to_ingest:
        match = fetch_match(match_id)


        if match['info']['queueId'] != 420:
            continue  # Only ingest ranked solo matches

        game_duration_sec = match["info"].get("gameDuration", 0) 

        if game_duration_sec < 15 * 60:
            continue

        formatted_match = format_match(match, puuid)

        timeline = fetch_match_timeline(match_id) # fetch events
    
        checkpoints = extract_timeline_checkpoints(timeline, match, puuid) # for match table
        formatted_match.update(checkpoints)

        db.insert_match(formatted_match)

        participant_id = get_participant_id(match, puuid)
        
        events = format_match_events(timeline, participant_id, puuid)
        
        for event in events:
            db.insert_event(event)

    return match_ids_to_ingest
