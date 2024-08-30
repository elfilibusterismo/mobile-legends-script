import os
import requests

def send_message(chat_id, token, message, topic_id=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    if topic_id:
        payload['message_thread_id'] = topic_id

    response = requests.post(url, data=payload)
    return response

if __name__ == "__main__":
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    COMMIT_AUTHOR = os.getenv('GITHUB_ACTOR')
    COMMIT_MESSAGE = os.getenv('COMMIT_MESSAGE')
    TELEGRAM_TOPIC_ID = os.getenv('TELEGRAM_TOPIC_ID', None)
    PLAYSTORE_URL = "https://play.google.com/store/apps/details?id=com.elfilibustero.origin"

    message = f"*Author:* {COMMIT_AUTHOR}\n" \
                f"{COMMIT_MESSAGE}\n\n" \
                f"🚀 [View App on Play Store]({PLAYSTORE_URL})"
    response = send_message(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, message, TELEGRAM_TOPIC_ID)
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")
