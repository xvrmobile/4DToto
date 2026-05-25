import os
import requests
from bs4 import BeautifulSoup
import json

def get_live_4d_data():
    url = "https://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/fourd_result_top_draws_en.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parse the official HTML table elements safely
        draw_date_text = soup.find('th', class_='draw-date').text.strip() if soup.find('th', class_='draw-date') else "Latest Draw"
        
        # Grab the top 3 prize blocks dynamically from the official table row
        prizes = [td.text.strip() for td in soup.find_all('td', class_='td-number')]
        
        # Guard clause: If the web structure returned empty arrays, raise fallback error
        if len(prizes) < 3:
            raise ValueError("Incomplete target table matrices returned.")
            
        return {
            "draw_date": draw_date_text,
            "first_prize": prizes[0],
            "second_prize": prizes[1],
            "third_prize": prizes[2],
            "starters": [td.text.strip() for td in soup.find_all('td', class_='td-starter')],
            "consolations": [td.text.strip() for td in soup.find_all('td', class_='td-consolation')]
        }
        
    except Exception as e:
        print(f"Live parsing error occurred: {e}")
        return None

def main():
    os.makedirs('data', exist_ok=True)
    
    # 1. Fetch real dynamic pools data
    live_data = get_live_4d_data()
    
    if not live_data:
        print("Scraper aborted: Data collection stream disconnected.")
        return

    # 2. Save the real numbers directly into your JSON data file repository
    with open('data/4d_latest.json', 'w') as f:
        json.dump(live_data, f, indent=4)
    print(f"Data manifest successfully updated for: {live_data['draw_date']}")

    # 3. Retrieve Environment Credentials
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Missing API token credentials. Telegram delivery skipped.")
        return

    # 4. Construct the Live, Real Notification Payload
    message = (
        "📢 *OFFICIAL SG POOLS DRAW COMPLETE* 📢\n\n"
        f"📅 *Draw Details:* {live_data['draw_date']}\n"
        f"🥇 *1st Prize:* `{live_data['first_prize']}`\n"
        f"🥈 *2nd Prize:* `{live_data['second_prize']}`\n"
        f"🥉 *3rd Prize:* `{live_data['third_prize']}`\n\n"
        "📱 Open your mobile scanner link to check your starter and consolation numbers instantly!"
    )

    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(telegram_url, json=payload)
    print(f"Telegram Broadcast Status: {response.status_code}")

if __name__ == "__main__":
    main()
