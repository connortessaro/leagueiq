import storage.db as db
from rules.types import RuleType


def evaluate_rules(match_id: str, puuid: str) -> list[RuleType]:
    features = db.get_features(match_id, puuid)
    curr_rules = []

    early_game_rules = early_game_check(features)
    
    curr_rules += early_game_rules
    economy_rules = economy_check(features)
    curr_rules += economy_rules
    objective_rules = objective_check(features)
    curr_rules += objective_rules
    damage_rules = combat_stat_check(features)
    curr_rules += damage_rules
    vision_rules = vision_check(features)
    curr_rules += vision_rules
    return curr_rules


def early_game_check(features: list[dict]) -> list[RuleType]:
    triggered_rules: list[RuleType] = []
    for feature in features:
        feature_name = feature["feature_name"]
        feature_value = feature["feature_value"]

        if feature_name == "early_death":
            rule = None
            if feature_value > 1:
                rule = RuleType(
                    rule_name="Early Deaths",
                    message="Player died more than once in the early game.",
                    severity=4,
                )
            else:
                rule = RuleType(
                    rule_name="Early Death",
                    message="Player died once in the early game.",
                    severity=3,
                )
            triggered_rules.append(rule)
        elif feature_name == "cs_at_10":
            rule = None

            if feature_value >= 70:
                rule = RuleType(
                    rule_name="Good Early CS",
                    message="Player had good creep score at 10 minutes.",
                    severity=1,
                )
            elif feature_value >= 50 and feature_value < 70:
                rule = RuleType(
                    rule_name="Decent Early CS",
                    message="Player had average creep score at 10 minutes.",
                    severity=2,
                )
            elif feature_value < 50:
                rule = RuleType(
                    rule_name="Poor Early CS",
                    message="Player had poor creep score at 10 minutes.",
                    severity=4,
                )
            triggered_rules.append(rule)
        elif feature_name == "gold_diff_at_15":
            gold_diff_at_15 = feature_value
            rule = None

            if gold_diff_at_15 >= 600:
                rule = RuleType(
                    rule_name="Strong Gold Lead",
                    message="Player had a strong gold lead at 15 minutes.",
                    severity=1,
                )
            elif gold_diff_at_15 >= 0 and gold_diff_at_15 < 600:
                rule = RuleType(
                    rule_name="Slight Gold Lead",
                    message="Player had a slight gold lead at 15 minutes.",
                    severity=2,
                )
            elif gold_diff_at_15 > -600 and gold_diff_at_15 < 0:
                rule = RuleType(
                    rule_name="Slight Gold Deficit",
                    message="Player had a slight gold deficit at 15 minutes.",
                    severity=3,
                )
            elif gold_diff_at_15 < -600:
                rule = RuleType(
                    rule_name="Significant Gold Deficit",
                    message="Player had a significant gold deficit at 15 minutes.",
                    severity=5,
                )
            triggered_rules.append(rule)
        elif feature_name == "xp_at_10":
            xp_at_10 = feature_value
            rule = None

            if xp_at_10 >= 5000:
                rule = RuleType(
                    rule_name="Good Early XP",
                    message="Player had good experience at 10 minutes.",
                    severity=1,
                )
            elif xp_at_10 >= 4000:
                rule = RuleType(
                    rule_name="Decent Early XP",
                    message="Player had average experience at 10 minutes.",
                    severity=2,
                )
            elif xp_at_10 < 4000:
                rule = RuleType(
                    rule_name="Poor Early XP",
                    message="Player had poor experience at 10 minutes.",
                    severity=4,
                )
            triggered_rules.append(rule)
    return triggered_rules


def economy_check(features: list[dict]) -> list[RuleType]:
    triggered_rules: list[RuleType] = []

    for feature in features:
        feature_name = feature["feature_name"]

        if feature_name == "gold_per_min":  # check if makes sense
            gpm = feature["feature_value"]
            rule = None

            if gpm >= 400:
                rule = RuleType(
                    rule_name="Excellent Gold Income",
                    message="Player had excellent gold income per minute.",
                    severity=1,
                )
            elif gpm >= 300 and gpm < 400:
                rule = RuleType(
                    rule_name="Good Gold Income",
                    message="Player had good gold income per minute.",
                    severity=2,
                )
            elif gpm >= 200 and gpm < 300:
                rule = RuleType(
                    rule_name="Average Gold Income",
                    message="Player had average gold income per minute.",
                    severity=3,
                )
            elif gpm < 200:
                rule = RuleType(
                    rule_name="Poor Gold Income",
                    message="Player had poor gold income per minute.",
                    severity=4,
                )
            triggered_rules.append(rule)
    return triggered_rules


def objective_check(features: list[dict]) -> list[RuleType]:
    # aggregate counts of objective participation
    counts = {}

    for feature in features:
        name = feature["feature_name"]
        if name in (
            "dragon_participation",
            "herald_participation",
            "baron_participation",
            "structure_participation",
        ):
            counts[name] = counts.get(name, 0) + feature["feature_value"] 

    triggered_rules: list[RuleType] = []

    # dragon rules
    dragon_count = None
    if "dragon_participation" in counts: # check if dragon feature exists
        dragon_count = counts["dragon_participation"]

    if dragon_count is None:
        pass
    elif dragon_count >= 4:
        triggered_rules.append(
            RuleType(
                rule_name="Great Dragon Participation",
                message="Player participated in four or more dragon kills.",
                severity=1,
            )
        )
    elif dragon_count >= 2:
        triggered_rules.append(
            RuleType(
                rule_name="Good Dragon Participation",
                message="Player participated in multiple dragon kills.",
                severity=2,
            )
        )
    elif dragon_count == 1:
        triggered_rules.append(
            RuleType(
                rule_name="Low Dragon Participation",
                message="Player participated in only one dragon kill.",
                severity=3,
            )
        )
    elif dragon_count == 0:
        triggered_rules.append(
            RuleType(
                rule_name="No Dragon Participation",
                message="Player did not participate in any dragon fights.",
                severity=4,
            )
        )

    # herald rules
    herald_count = None

    if 'herald_participation' in counts:
        herald_count = counts['herald_participation']

    if herald_count is None:
        pass
    elif herald_count == 0:
        triggered_rules.append(
            RuleType(
                rule_name="No Herald Participation",
                message="Player did not participate in Rift Herald.",
                severity=3,
            )
        )
    elif herald_count >= 1:
        triggered_rules.append(
            RuleType(
                rule_name="Herald Participation",
                message="Player participated in Rift Herald.",
                severity=1,
            )
        )

    baron_count = None
    if 'baron_participation' in counts:
        baron_count = counts.get("baron_participation", 0)

    if baron_count is None:
        pass
    elif baron_count == 0:
        triggered_rules.append(
            RuleType(
                rule_name="No Baron Participation",
                message="Player was not present for Baron fights.",
                severity=3,
            )
        )
    elif baron_count >= 1:
        triggered_rules.append(
            RuleType(
                rule_name="Baron Participation",
                message="Player participated in Baron fights.",
                severity=1,
            )
        )

    # structure rules
    structure_count = None
    if 'structure_participation' in counts:
        structure_count = counts['structure_participation']

    if structure_count is None:
        pass
    elif structure_count == 0:
        triggered_rules.append(
            RuleType(
                rule_name="No Structure Pressure",
                message="Player was not involved in taking towers or inhibitors.",
                severity=4,
            )
        )
    elif structure_count >= 4:
        triggered_rules.append(
            RuleType(
                rule_name="Strong Structure Pressure",
                message="Player was heavily involved in taking structures.",
                severity=1,
            )
        )

    return triggered_rules


def combat_stat_check(features: list[dict]) -> list[RuleType]:
    triggered_rules: list[RuleType] = []

    for feature in features:
        feature_name = feature["feature_name"]

        if feature["feature_name"] == "kill_participation":
            kp = feature["feature_value"]
            rule = None

            if kp >= 70:
                rule = RuleType(
                    rule_name="Excellent Kill Participation",
                    message="Player had excellent kill participation.",
                    severity=1,
                )
            elif kp >= 50 and kp < 70:
                rule = RuleType(
                    rule_name="Good Kill Participation",
                    message="Player had good kill participation.",
                    severity=2,
                )
            elif kp >= 30 and kp < 50:
                rule = RuleType(
                    rule_name="Average Kill Participation",
                    message="Player had average kill participation.",
                    severity=3,
                )
            elif kp < 30:
                rule = RuleType(
                    rule_name="Poor Kill Participation",
                    message="Player had poor kill participation.",
                    severity=4,
                )
            triggered_rules.append(rule)
        elif feature["feature_name"] == "damage_per_min":
            dpm = feature["feature_value"]
            rule = None

            if dpm < 300:
                rule = RuleType(
                    rule_name="Low Damage Output",
                    message="Player had low damage per minute.",
                    severity=5,
                )
            elif dpm >= 300 and dpm < 450:
                rule = RuleType(
                    rule_name="Below Average Damage Output",
                    message="Player had below average damage per minute.",
                    severity=4,
                )
            elif dpm >= 450 and dpm < 650:
                rule = RuleType(
                    rule_name="Average Damage Output",
                    message="Player had average damage per minute.",
                    severity=3,
                )
            elif dpm >= 650 and dpm < 850:
                rule = RuleType(
                    rule_name="High Damage Output",
                    message="Player had high damage per minute.",
                    severity=1,
                )
            elif dpm >= 850:
                rule = RuleType(
                    rule_name="Very High Damage Output",
                    message="Player had very high damage per minute.",
                    severity=1,
                )
            triggered_rules.append(rule)
    return triggered_rules


def vision_check(features: list[dict]) -> list[RuleType]:
    triggered_rules: list[RuleType] = []

    for feature in features:
        feature_name = feature["feature_name"]

        if feature["feature_name"] == "vision_score_per_min":
            vspm = feature["feature_value"]
            rule = None

            if vspm >= 1.6:
                rule = RuleType(
                    rule_name="Excellent Vision Control",
                    message="Player had excellent vision score per minute.",
                    severity=1,
                )
            elif vspm >= 1.2:
                rule = RuleType(
                    rule_name="Good Vision Control",
                    message="Player had good vision score per minute.",
                    severity=2,
                )
            elif vspm >= 0.8:
                rule = RuleType(
                    rule_name="Average Vision Control",
                    message="Player had average vision score per minute.",
                    severity=3,
                )
            else:
                rule = RuleType(
                    rule_name="Poor Vision Control",
                    message="Player had poor vision score per minute.",
                    severity=4,
                )
            triggered_rules.append(rule)
    return triggered_rules
