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
    COMMIT_MESSAGE = os.getenv('COMMIT_MESSAGE')
    TELEGRAM_TOPIC_ID = os.getenv('TELEGRAM_TOPIC_ID', None)

    message = f"New commit in `{os.getenv('GITHUB_REPOSITORY')}`:\n\n{COMMIT_MESSAGE}"
    
    response = send_message(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, message, TELEGRAM_TOPIC_ID)
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")
