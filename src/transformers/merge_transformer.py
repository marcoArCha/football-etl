import pandas as pd
from loguru import logger
from typing import Optional


def flatten_player(raw: dict) -> Optional[dict]:
    """
    Flattens a single raw player dict from the API into a clean flat dict.

    Args:
        raw: raw player dict from the API response

    Returns:
        Flat dict with player info and stats, or None if data is invalid
    """
    try:
        player = raw.get("player", {})
        stats = raw.get("statistics", [])

        if not stats:
            logger.warning(f"No statistics for player: {player.get('name', 'unknown')}")
            return None

        # Pick the stats entry with the most data (not just the first one)
        # We rank by appearances — the team where they played most is the primary one
        stat = max(stats, key=lambda s: s.get("games", {}).get("appearences") or 0)

        return {
            # Player info
            "player_id":        player.get("id"),
            "name":             player.get("name"),
            "age":              player.get("age"),
            "nationality":      player.get("nationality"),
            "position":         stat.get("games", {}).get("position"),

            # Team
            "team":             stat.get("team", {}).get("name"),

            # Games
            "appearances":      stat.get("games", {}).get("appearences"),
            "minutes_played":   stat.get("games", {}).get("minutes"),
            "rating":           stat.get("games", {}).get("rating"),

            # Goals
            "goals":            stat.get("goals", {}).get("total"),
            "assists":          stat.get("goals", {}).get("assists"),

            # Passes
            "pass_accuracy":    stat.get("passes", {}).get("accuracy"),
            "key_passes":       stat.get("passes", {}).get("key"),

            # Defense
            "tackles":          stat.get("tackles", {}).get("total"),
            "interceptions":    stat.get("tackles", {}).get("interceptions"),

            # Duels
            "duels_total":      stat.get("duels", {}).get("total"),
            "duels_won":        stat.get("duels", {}).get("won"),

            # Cards
            "yellow_cards":     stat.get("cards", {}).get("yellow"),
            "red_cards":        stat.get("cards", {}).get("red"),
        }

    except Exception as e:
        logger.error(f"Failed to flatten player: {e}")
        return None


def transform(players_raw: list[dict]) -> list[dict]:
    logger.info(f"Starting transformation for {len(players_raw)} players")

    flattened = [flatten_player(p) for p in players_raw]
    clean = [p for p in flattened if p is not None]

    df = pd.DataFrame(clean)

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["player_id"])
    after = len(df)

    if before != after:
        logger.warning(f"Dropped {before - after} duplicate players")

    # Fix rating — convert string to float
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["rating"] = df["rating"].apply(lambda x: round(x, 2) if pd.notna(x) else None)

    # Replace all NaN with None
    df = df.astype(object).where(pd.notna(df), other=None)

    # Convert to dict first, THEN fix int types
    result = df.to_dict(orient="records")

    int_columns = [
        "appearances", "minutes_played", "goals", "assists",
        "key_passes", "tackles", "interceptions", "duels_total",
        "duels_won", "yellow_cards", "red_cards"
    ]

    # Now we're working with plain Python dicts — None stays None, no pandas interference
    for player in result:
        for col in int_columns:
            if player[col] is not None:
                player[col] = int(player[col])

    logger.success(f"Transformation complete — {len(result)} clean players ready")
    return result