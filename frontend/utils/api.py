import requests

BASE_URL = "http://localhost:8001/api/v1"


def get_top_runs():
    return requests.get(
        f"{BASE_URL}/players/top-runs"
    ).json()


def get_top_strike_rates():
    return requests.get(
        f"{BASE_URL}/players/top-strike-rate"
    ).json()


def get_player_career(player_name):
    return requests.get(
        f"{BASE_URL}/players/{player_name}/career"
    ).json()


def get_player_seasons(player_name):
    return requests.get(
        f"{BASE_URL}/players/{player_name}/season-trend"
    ).json()


def get_top_wickets():
    return requests.get(
        f"{BASE_URL}/bowlers/top-wickets"
    ).json()


def get_best_economy():
    return requests.get(
        f"{BASE_URL}/bowlers/best-economy"
    ).json()


def get_top_rivalries():
    return requests.get(
        f"{BASE_URL}/matchups/top-rivalries/list"
    ).json()


def get_high_scoring_venues():
    return requests.get(
        f"{BASE_URL}/venues/highest-scoring"
    ).json()


def get_run_trends():
    return requests.get(
        f"{BASE_URL}/seasons/run-trends"
    ).json()


def get_matchup(batter_name, bowler_name):
    return requests.get(
        f"{BASE_URL}/matchups/{batter_name}/{bowler_name}"
    ).json()