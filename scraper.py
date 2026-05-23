import os
import requests
import json

def force_push_message():
    # 1. Force establish the data directories
    os.makedirs('data', exist_ok=True)
    
    draw_data = {
        "draw_date": "2026-05-20",
        "first_prize": "7699",
        "second_prize": "9517",
        "third_prize": "8945",
        "starters": ["1117", "2873", "3075", "3722"],
        "consolations": ["0582", "0706", "2066", "2314"]
    }
    
    with open('data/4d_latest.json', 'w') as f:
        json.dump(draw_data, f)

    # 2. Extract Secrets
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Missing API credential configuration flags.")
        return

    # 3. Create a clean message that doesn't use risky formatting characters
    message = (
        "🎉 SYSTEM TESTING: ALERTS CHANNELS ACTIVE 🎉\n\n"
        "📅 Draw Date: 2026-05-20\n"
        "🥇 1st Prize: 7699\n"
        "🥈 2nd Prize: 9517\n"
        "🥉 3rd Prize: 8945\n\n"
        "🎫 Scanned Bet Matcher Status: ONLINE\n"
        "🚀 Everything is linked! Your notifications are officially breaking through."
    )

    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    # Send request and print exactly what Telegram tells us
    response = requests.post(telegram_url, json=payload)
    print(f"Telegram Server Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    force_push_message()
