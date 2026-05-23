import os
import requests
import json

def send_telegram_push(message_text):
    # Retrieve secrets securely from the GitHub runner environment
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Missing Telegram Credentials.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "MarkdownV2" # Allows for bold and monospaced font styling
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Telegram alert pushed successfully!")
    else:
        print(f"Failed to send: {response.text}")

def check_my_bets_and_notify():
    # 1. Load the winning numbers we just scraped
    with open('data/4d_latest.json', 'r') as f:
        results = json.load(f)
        
    # 2. Load your active scanned tickets (saved previously from your frontend app)
    # Let's mock a user's scanned ticket array for this example:
    my_tickets = [
        {"draw_date": "2026-05-20", "number": "1234", "type": "Big", "amount": 5}
    ]
    
    for ticket in my_tickets:
        if ticket["draw_date"] == results["draw_date"]:
            win_amount = 0
            prize_tier = ""
            
            # Simple 4D matching example logic
            if ticket["number"] == results["first_prize"]:
                win_amount = ticket["amount"] * 2000 if ticket["type"] == "Big" else ticket["amount"] * 3000
                prize_tier = "1st Prize 🏆"
            # ... repeat logic loops for 2nd, 3rd, starters, etc ...

            # 3. Construct the clean message layout
            # (Note: Characters like '-', '.', '!' must be escaped with a backslash in MarkdownV2)
            if win_amount > 0:
                msg = (
                    f"🎉 *HUAT AH\! WINNING ALERT* 🎉\n\n"
                    f"📅 *Draw Date:* {ticket['draw_date']}\n"
                    f"🎫 *Bet Number:* `{ticket['number']}`\n"
                    f"📈 *Tier:* {prize_tier}\n"
                    f"💰 *Total Won:* SGD ${win_amount:,.2f}"
                ).replace("-", "\-").replace(".", "\.")
            else:
                msg = (
                    f"😢 *No Win This Time* 😢\n\n"
                    f"📅 *Draw Date:* {ticket['draw_date']}\n"
                    f"🎫 *Bet Number:* `{ticket['number']}`\n"
                    f"Status: Try again next draw\!"
                ).replace("-", "\-")
                
            send_telegram_push(msg)

if __name__ == "__main__":
    check_my_bets_and_notify()
