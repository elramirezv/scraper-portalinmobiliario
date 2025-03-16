import os

import requests

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
    """
    Envía un mensaje a un bot de Telegram.

    Args:
        bot_token (str): El token de tu bot de Telegram
        chat_id (str): El ID del chat donde quieres enviar el mensaje
        message (str): El mensaje que quieres enviar

    Returns:
        dict: La respuesta de la API de Telegram
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    response = requests.post(url, data=payload)
    return response.json()
