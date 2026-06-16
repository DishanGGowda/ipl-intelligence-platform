from src.utils.yaml_parser import (
    load_match,
    extract_match_info,
    extract_teams,
    extract_players,
    extract_innings,
    extract_deliveries,
)


TEST_FILE = r"C:\Users\disha\ipl-intelligence-platform\data\cricsheet\1254087.yaml"


def test_load_match():
    match = load_match(TEST_FILE)
    assert match is not None


def test_extract_match_info():
    match = load_match(TEST_FILE)
    info = extract_match_info(match)

    assert "teams" in info
    assert "venue" in info


def test_extract_teams():
    match = load_match(TEST_FILE)
    teams = extract_teams(match)

    assert len(teams) == 2


def test_extract_players():
    match = load_match(TEST_FILE)
    players = extract_players(match)

    assert len(players) == 2


def test_extract_innings():
    match = load_match(TEST_FILE)
    innings = extract_innings(match)

    assert len(innings) > 0


def test_extract_deliveries():
    match = load_match(TEST_FILE)
    deliveries = extract_deliveries(match)

    assert len(deliveries) > 0