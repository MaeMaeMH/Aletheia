import os
import requests
import json
import logging
from dotenv import load_dotenv
import game_params

load_dotenv()

# === Loggin Setup ===
# Directory to store log files
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "update_alert.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


USER_KEY = os.getenv("PUSHOVER_USER_KEY")
API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
DEVICE_NAME = os.getenv("PUSHOVER_DEVICE_NAME")

STEAM_NEWS_URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"

# Directory to store state files (last notified news)
STATE_DIR = "state_files"
os.makedirs(STATE_DIR, exist_ok=True)  # Ensure the directory exists

def send_pushover(message):
    logging.info(f"Sending Pushover notification: {message[:100]}..." if len(message) > 100 else message) # Log full message if short, else preview (100 chars)
    try:
        r = requests.post(
            "https://api.pushover.net/1/messages.json",
            params={
                "token": API_TOKEN,
                "user": USER_KEY,
                "message": message,
                "html": 1,                  # Enable HTML formatting in the message
                "device": DEVICE_NAME,      # Target device
                "priority": 2,              # Emergency priority
                "retry": 30,                # Retry interval in seconds for emergency priority
                "expire": 600,              # Expiration time in seconds for emergency priority
                "sound": "Navi_Hey_Listen"  # Custom notification sound
            },
        )
        r.raise_for_status()
        logging.info("Pushover notification sent successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to send Pushover notification: {e}")
    
def main():
    # Collect all game parameters from game_params module
    games = {name: getattr(game_params, name) for name in dir(game_params) if name.endswith("_PARAMS")}

    for game_var, params in games.items():
        
        game_name = params.get("name", game_var) # Cleaner game name for display
        state_file = os.path.join(STATE_DIR, f"{game_name}_last_update.txt")
        
        logging.info("---" * 10)
        logging.info(f"Checking news for {game_name}")
        
        # Load previously notified news IDs or initialize an empty list
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                last_notified_gids = json.load(f)
        else:
            last_notified_gids = []
                
        # Fetch news for the game from Steam API
        response = requests.get(STEAM_NEWS_URL, params=params)
        try:
            feed = response.json()
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON for {game_name}: {response.text[:200]} ..." if len(response.text) > 200 else response.text) # Log full response if short, else preview (200 chars)
            continue

        # Extract news items from the API response
        news_items = feed.get("appnews", {}).get("newsitems", [])
        
        # Copy previous state to update with newly notified items
        new_gids = last_notified_gids.copy()
        for item in reversed(news_items):  # Process older items first
            gid = item.get("gid", "")
            title = item.get("title", "")
            url = item.get("url", "")
            
            # Send notification only for news items not already notified
            if gid and gid not in last_notified_gids:
                logging.info(f"New update found for {game_name}: {title}")
                send_pushover(f'⚠️ {game_name} Update incoming:\n<a href="{url}">Click here</a> for your patchnotes.\nAnd get out of bed now lazy ass!')
                new_gids.append(gid)
            else:
                logging.info(f"No new Update found for {game_name}")
            
        # Keep only the last 'count' number of news items to limit state file size
        count = params.get("count")
        new_gids = new_gids[-count:]
        
        # Save updated list of notified news IDs
        with open(state_file, "w") as f:
            json.dump(new_gids, f)
    
    logging.info("Finished checking all games")
    logging.info("---" * 10)
        
if __name__ == "__main__":
    main()
