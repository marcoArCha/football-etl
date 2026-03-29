import requests
from loguru import logger
from config.settings import API_FOOTBALL_KEY, API_HOST, BASE_URL, LEAGUE_ID, SEASON


def get_players(page: int = 1) -> list[dict]:
    """
    Fetches players from API-Football for a given league and season.

    Args:
        page: pagination page number (API returns 20 players per page)

    Returns:
        List of player dicts from the API response
    """
    url = f"{BASE_URL}/players"

    headers = {
        "x-apisports-key": API_FOOTBALL_KEY,
        "x-apisports-host": API_HOST,
    }

    params = {
        "league": LEAGUE_ID,
        "season": SEASON,
        "page": page,
    }

    logger.info(f"Fetching players — league={LEAGUE_ID}, season={SEASON}, page={page}")

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()  # lanza excepción si status != 200

    data = response.json()

    # El API envuelve la data en "response"
    players = data.get("response", [])
    total_pages = data.get("paging", {}).get("total", 1)

    logger.success(f"Fetched {len(players)} players from page {page}/{total_pages}")

    return players, total_pages


def extract_all_players() -> list[dict]:
    """
    Fetches ALL pages of players and returns them as a single list.

    Returns:
        Full list of player dicts
    """
    all_players = []

    first_page, total_pages = get_players(page=1)
    all_players.extend(first_page)

    # Si hay más páginas, las traemos todas
    # OJO: con 100 requests/día, limitamos a 3 páginas (60 jugadores)
    max_pages = min(total_pages, 3)

    for page in range(2, max_pages + 1):
        players, _ = get_players(page=page)
        all_players.extend(players)

    logger.info(f"Total players extracted: {len(all_players)}")
    return all_players