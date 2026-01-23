import storage.db as db


def extract_features(match_id: str, puuid: str) -> list[dict]:
    match = db.get_match(match_id, puuid)
    game_duration = match["game_duration"]
    features = []
    minutes = game_duration / 60

    # match table features
    features.append(
        {
            "feature_name": "gold_per_min",
            "feature_value": match["gold_earned"] / minutes,
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "gold_total",
            "feature_value": match["gold_earned"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "kda_ratio",
            "feature_value": match["kill_participation"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "cs_total",
            "feature_value": match["lane_minions_killed"]
            + match["jungle_minions_killed"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "cs_per_min",
            "feature_value": match["game_cs_per_minute"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "vision_score_per_min",
            "feature_value": float(match["vision_score"] / minutes),
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "damage_per_min",
            "feature_value": match["total_damage_dealt_to_champions"] / minutes,
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )

    # checkpoint features from match table
    features.append(
        {
            "feature_name": "gold_at_10",
            "feature_value": match["gold_at_10"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "cs_at_10",
            "feature_value": match["cs_at_10"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "xp_at_10",
            "feature_value": match["xp_at_10"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )
    features.append(
        {
            "feature_name": "gold_diff_at_15",
            "feature_value": match["gold_diff_at_15"],
            "match_id": match["match_id"],
            "puuid": match["puuid"],
        }
    )

    events = db.get_events(match_id, puuid)
    # features from events
    for event in events:
        event_feat = event_features(event)
        if event_feat:
            features.append(event_feat)
    return features


def event_features(event: dict) -> dict | None:
    feature_name = None
    feature_value = 0
    if event["event_type"] == "DRAGON_PARTICIPATION":
        feature_name = "dragon_participation"
        feature_value = 1
        return {
            "feature_name": feature_name,
            "feature_value": feature_value,
            "match_id": event["match_id"],
            "puuid": event["puuid"],
        }
    if event["event_type"] == "RIFT_HERALD_PARTICIPATION":
        feature_name = "herald_participation"
        feature_value = 1
        return {
            "feature_name": feature_name,
            "feature_value": feature_value,
            "match_id": event["match_id"],
            "puuid": event["puuid"],
        }
    if event["event_type"] == "BARON_PARTICIPATION":
        feature_name = "baron_participation"
        feature_value = 1
        return {
            "feature_name": feature_name,
            "feature_value": feature_value,
            "match_id": event["match_id"],
            "puuid": event["puuid"],
        }
    if event["event_type"] == "EARLY_DEATH":
        feature_name = "early_death"
        feature_value = 1
        return {
            "feature_name": feature_name,
            "feature_value": feature_value,
            "match_id": event["match_id"],
            "puuid": event["puuid"],
        }
    if event["event_type"] == "STRUCTURE_PARTICIPATION":
        feature_name = "structure_participation"
        feature_value = 1
        return {
            "feature_name": feature_name,
            "feature_value": feature_value,
            "match_id": event["match_id"],
            "puuid": event["puuid"],
        }
    return None


def build_features(match_id: str, puuid: str) -> int:
    """
    Returns the number of features built
    """
    if db.features_exist(match_id, puuid):
        return 0
    features = extract_features(match_id, puuid)
    for feature in features:
        db.insert_feature(feature)
    return len(features)
