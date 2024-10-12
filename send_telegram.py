import os
import requests
import json

def escape_markdown_v2(text):
    escape_chars = r'_~`#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

def send_message(chat_id, token, message, topic_id=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': escape_markdown_v2(message),
        'parse_mode': 'MarkdownV2'
    }
    if topic_id:
        payload['message_thread_id'] = topic_id

    response = requests.post(url, data=payload)
    return response

if __name__ == "__main__":
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    TELEGRAM_TOPIC_ID = os.getenv('TELEGRAM_TOPIC_ID', None)
    PLAYSTORE_URL = "https://play.google.com/store/apps/details?id=com.elfilibustero.origin"
    
    commits = os.getenv('GITHUB_EVENT_PATH')
    commit_messages = []

    with open(commits, 'r') as f:
        data = json.load(f)
        for commit in data['commits']:
            commit_messages.append(f">{commit['message']}")

    commit_messages_str = "\n".join(commit_messages)

    message = f"{commit_messages_str}\n\n" \
                f"🚀 [View App on Play Store]({PLAYSTORE_URL})"
    response = send_message(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, message, TELEGRAM_TOPIC_ID)
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")
