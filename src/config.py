# Playtime ranges for categorisation (in hours)
CATEGORY_RANGES = {
    "Quick Bites (<2h)": (0, 2),
    "Short (2–5h)": (2, 5),
    "Medium (5–15h)": (5, 15),
    "Long (15–40h)": (15, 40),
    "Epic (>40h)": (40, float("inf")),
    "Multiplayer/Endless": None  # Special case for non-categorisable games
}

# Additional configurations can be added here
OUTPUT_FORMAT = "console"  # Options: "console", "json", "csv"
