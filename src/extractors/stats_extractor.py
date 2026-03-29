import requests
from loguru import logger
from config.settings import API_FOOTBALL_KEY, API_HOST, BASE_URL, LEAGUE_ID, SEASON
from typing import Optional


def get_player_stats(player_id: int) -> Optional[dict]:
    """
    Fetches statistics for a single player.

    Args:
        player_id: the player's ID from API-Football

    Returns:
        Dict with player stats, or None if request fails
    """
    url = f"{BASE_URL}/players"

    headers = {
        "x-apisports-key": API_FOOTBALL_KEY,
        "x-apisports-host": API_HOST,
    }

    params = {
        "id": player_id,
        "league": LEAGUE_ID,
        "season": SEASON,
    }

    logger.info(f"Fetching stats for player_id={player_id}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get("response", [])

        if not results:
            logger.warning(f"No stats found for player_id={player_id}")
            return None

        return results[0]  # retorna el primer (y único) resultado

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch stats for player_id={player_id}: {e}")
        return None


def extract_all_stats(players: list[dict]) -> list[dict]:
    """
    Fetches stats for a list of players.

    Args:
        players: list of player dicts from players_extractor

    Returns:
        List of player stats dicts
    """
    all_stats = []

    for player_data in players:
        player_id = player_data.get("player", {}).get("id")

        if not player_id:
            logger.warning("Player without ID found, skipping...")
            continue

        stats = get_player_stats(player_id)

        if stats:
            all_stats.append(stats)

    logger.info(f"Total stats extracted: {len(all_stats)}")
    return all_stats