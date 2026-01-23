from ingest.ingest_pipeline import ingest_account, ingest_matches
from features.feature_builder import build_features
import storage.db as db
from rules.rules_engine import evaluate_rules
from report.report_builder import build_match_report


def main():
    riot_id = input("Enter Riot ID (format: Name#Tagline): \n")

    if "#" not in riot_id:
        print("Invalid Riot ID format. Please use the format Name#Tagline.")
        return

    db.open_connection()
    db.init_db()

    gameName, tagLine = riot_id.split("#")

    puuid = ingest_account(gameName, tagLine)

    count_input = input(
        "How many recent matches would you like to ingest? (Default is 20): \n"
    )
    ingest_matches(puuid, int(count_input) if count_input.strip() else 20)

    index = 0
    match_ids: list[str] = db.get_match_ids_by_puuid(puuid)

    # ingest events and then features

    while True:
        print(f"Displaying match {index + 1} of {len(match_ids)}")
        match_id = match_ids[index]
        build_features(match_id, puuid)

        rules = evaluate_rules(match_id, puuid)

        isWin = db.get_match(match_id, puuid)["win"]

        report = build_match_report(rules, isWin)
        print(report + "\n")
        cmd = input(
            "Type 'n' for next match, 'p' for previous match, or 'q' to quit: \n"
        ).lower()

        if cmd == "n" and index < len(match_ids) - 1:
            index += 1
        if cmd == "p" and index > 0:
            index -= 1
        if cmd == "q":
            print("Exiting the program.")
            db.close_connection()
            break


if __name__ == "__main__":
    main()
