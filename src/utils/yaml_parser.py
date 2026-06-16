from pathlib import Path
import yaml


def load_match(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_match_info(match):
    return match["info"]


def extract_teams(match):
    return match["info"]["teams"]


def extract_players(match):
    return match["info"]["players"]


def extract_innings(match):
    return match["innings"]

def extract_deliveries(match):
    """
    Flatten all deliveries from a match.
    """

    deliveries = []

    innings_list = match["innings"]

    for innings_number, innings in enumerate(innings_list, start=1):

        innings_name = list(innings.keys())[0]

        innings_data = innings[innings_name]

        team = innings_data["team"]

        for delivery in innings_data["deliveries"]:

            ball = list(delivery.keys())[0]

            data = delivery[ball]

            deliveries.append(
                {
                    "innings": innings_number,
                    "batting_team": team,
                    "ball": ball,
                    "batsman": data.get("batsman"),
                    "non_striker": data.get("non_striker"),
                    "bowler": data.get("bowler"),
                    "runs_batsman": data["runs"]["batsman"],
                    "runs_extras": data["runs"]["extras"],
                    "runs_total": data["runs"]["total"],
                }
            )

    return deliveries