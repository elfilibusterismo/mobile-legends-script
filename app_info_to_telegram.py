import os
import json
import requests
import re

def escape_markdown(text: str, version: int = 1, entity_type: str = None) -> str:
    """
    Helper function to escape telegram markup symbols.

    Args:
        text (:obj:`str`): The text.
        version (:obj:`int` | :obj:`str`): Use to specify the version of telegrams Markdown.
            Either ``1`` or ``2``. Defaults to ``1``.
        entity_type (:obj:`str`, optional): For the entity types ``PRE``, ``CODE`` and the link
            part of ``TEXT_LINKS``, only certain characters need to be escaped in ``MarkdownV2``.
            See the official API documentation for details. Only valid in combination with
            ``version=2``, will be ignored else.
    """
    if int(version) == 1:
        escape_chars = r'_*`['
    elif int(version) == 2:
        if entity_type in ['pre', 'code']:
            escape_chars = r'\`'
        elif entity_type == 'text_link':
            escape_chars = r'\)'
        else:
            escape_chars = r'_*[]()~`>#+-=|{}.!'
    else:
        print('Markdown version must be either 1 or 2!')

    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


def send_message(chat_id, token, message, topic_id=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': escape_markdown(message),
        'parse_mode': 'MarkdownV2'
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

    message = (
        f"*Date*: {generated_at}\n\n"
        f"*Rating*: {app_details.get('score')}\n"
        f"*Installs*: {app_details.get('realInstalls')}\n\n"
        f"*Latest Reviews*\n"
    )

    for review in reviews:
        author = review.get("userName", "Anonymous")
        content = review.get("content", "No content")
        score = review.get("score", "N/A")
        message += (
            f"*User*: {escape_markdown(author)}\n"
            f"*Rating*: {score}\n"
            f"*Review*: {escape_markdown(content)}\n\n"
        )

    send_message(chat_id, bot_token, message, topic_id)