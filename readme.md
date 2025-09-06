# CS2 Update Alert

**Short Description:**  
This project automatically sends push notifications to your phone whenever a **CS2 update** is announced. Notifications are sent via **Pushover** and can wake you up at night (critical alert).

---

## Features
- Monitors official CS2 news (patch/update/release) via Steam Web API.  
- Filters only relevant updates, ignoring minor changes.  
- Push notifications sent directly to your phone (Pushover, priority = 2).  
- Stores the last update locally to avoid duplicate alerts.  

---

## Requirements
- Python 3.10+  
- Packages (install with `pip install -r requirements.txt`):  
  - `requests`  
  - `python-dotenv`  
  - `feedparser` (optional if using RSS feeds)  

---

## Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/MaeMaeMH/cs2_update_alert.git
   cd cs2_update_alert
