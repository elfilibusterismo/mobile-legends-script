import os
import json
import requests
import re
from datetime import datetime

def escape_special_chars(text: str) -> str:
    escape_chars = r'_~`#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

def format_date(iso_date: str) -> str:
    date_obj = datetime.fromisoformat(iso_date)
    return date_obj.strftime("%B %d, %Y, %I:%M %p")

def send_message(chat_id, token, message, topic_id=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    if topic_id:
        payload['message_thread_id'] = topic_id

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Message sent successfully to Telegram.")
    else:
        print(f"Failed to send message. Error: {response.text}")

if __name__ == "__main__":
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    topic_id = os.getenv('TELEGRAM_TOPIC_ID', None)

    json_file_path = "data/app_data.json"

    try:
        with open(json_file_path, "r") as file:
            combined_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {json_file_path} not found.")
        exit(1)

    app_details = combined_data.get("app_details", {})
    reviews = combined_data.get("reviews", [])
    generated_at = combined_data.get("generated_at", "Unknown")
    formatted_date = format_date(generated_at)

    message = (
        f"====================\n"
        f"📅 Date: {formatted_date}\n"
        f"====================\n\n"
        f"📊 App Details:\n"
        f"  - Rating: {round(float(app_details.get('score', 0)), 2)}\n"
        f"  - Installs: {format(int(app_details.get('realInstalls', 0)), ',')}\n\n"
        f"🌟 Latest Reviews:\n"
        f"--------------------\n"
    )

    for review in reviews:
        author = review.get("userName", "Anonymous")
        content = review.get("content", "No content")
        score = review.get("score", "N/A")
        message += (
            f"👤 User: {escape_special_chars(author)}\n"
            f"⭐ Rating: {score}\n"
            f"💬 Review: {escape_special_chars(content)}\n"
            f"--------------------\n"
        )

    send_message(chat_id, bot_token, message, topic_id)