import os
import json
import time

def get_cache_dir():
    """
    Get the cache directory in the user's Documents folder.
    """
    if os.name == 'nt':  # Windows
        base_dir = os.environ.get("USERPROFILE") or os.path.expanduser("~")
        docs_dir = os.path.join(base_dir, "Documents")
    else:  # macOS/Linux
        docs_dir = os.path.expanduser("~/Documents")

    cache_dir = os.path.join(docs_dir, "Steam Game Sorter")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        print(f"Cache directory created at: {cache_dir}")  # Inform user on first creation
    return cache_dir

def save_cache(data, filename):
    """
    Save data to a JSON file in the cache directory.
    """
    cache_dir = get_cache_dir()
    filepath = os.path.join(cache_dir, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file)

def load_cache(filename, max_age=None):
    """
    Load cached data if available and not expired.
    """
    cache_dir = get_cache_dir()
    filepath = os.path.join(cache_dir, filename)
    if not os.path.exists(filepath):
        return None

    if max_age:
        # Check if the cache is outdated
        file_age = time.time() - os.path.getmtime(filepath)
        if file_age > max_age:
            return None

    with open(filepath, 'r') as file:
        return json.load(file)
