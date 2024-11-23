import yaml

with open("categories.yml", "r") as file:
    CATEGORY_RANGES = yaml.safe_load(file)["categories"]

# Additional configurations can be added here
OUTPUT_FORMAT = "console"  # Options: "console", "json", "csv"
