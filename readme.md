# CS2 Update Alert

**Short Description:**  
This project automatically sends push notifications to your phone whenever a **CS2 update** or any monitored game update is announced. Notifications are sent via **Pushover** with emergency priority, retry intervals, and custom sounds.

---

## Features
- Monitors official game news via **Steam Web API**.  
- Tracks multiple games defined in `game_params.py`.  
- Sends push notifications for new updates only (avoids duplicates).  
- Stores last notified news locally (`state_files/`) to maintain state between runs.  
- Supports HTML formatting in notifications and custom notification sounds.  

---

## Requirements
- Python 3.10+  
- Packages (install with `pip install -r requirements.txt`):  
  - `requests`  
  - `python-dotenv`  

---

## Installation

1. Clone or download the repository:
    ```bash
    git clone https://github.com/MaeMaeMH/cs2_update_alert.git
    cd cs2_update_alert
    ```

2. Create a `.env` file with your Pushover credentials:
    ```env
    PUSHOVER_USER_KEY=your_user_key
    API_TOKEN=your_api_token
    ```

3. Ensure you have a `game_params.py` file defining your monitored games:
    ```python
    CS2_PARAMS = {
        "appid": 730,               # Example App ID (this one is for CS2)
        "count": 3,                 # Number of news items to track
        "tags": "patchnotes",       # Simple filter
        "name": "Counter-Strike 2"  # Only used for sending Pushover messages
    }
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the script:
    ```bash
    python main.py
    ```

---

## Adding More Games

You can monitor multiple games by defining additional `_PARAMS` dictionaries in `game_params.py`.  

- Refer to this **steam forum page** to find the game's AppID: https://steamcommunity.com/discussions/forum/0/4328600953647375080/
- Copy the template below and adjust for each new game:

  ```python
  # Template for adding a new game
  GAME_NAME_PARAMS = {
      "appid": 123456,       # Steam App ID of the game
      "count": 3,            # Number of latest news items to track
      "tags": "patchnotes",  # Optional: any custom tag/filter you want
      "name": "Game Name"    # Display name used in notifications
  }

## API Documentation

- **Pushover API** - Full documentation for notifications, priority, retry, expire, and sounds: https://pushover.net/api
- **Steam Web API** - Helpful reference for app IDs, news, and other endpoints: https://steamapi.xpaw.me/