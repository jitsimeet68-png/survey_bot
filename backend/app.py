import os
import logging
from uuid import UUID
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()  # грузим .env, если есть (в dev-режиме удобно)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Конфиг из окружения
BOTX_CTS_URL = os.getenv("BOTX_CTS_URL", "https://chat.example.ru")
BOTX_BOT_ID = os.getenv("BOTX_BOT_ID", "")
BOTX_SECRET = os.getenv("BOTX_SECRET", "")

@app.get("/healthz")
def healthz():
    return jsonify(ok=True), 200

@app.post("/api/v1/command")
def handle_command():
    """
    Webhook от eXpress BotX.
    Возвращаем 202 быстро, логику делаем сразу (MVP) или в фоне в будущем.
    """
    try:
        payload = request.get_json(force=True, silent=False)
    except Exception:
        app.logger.exception("Invalid JSON")
        return "", 400

    app.logger.info("Incoming command: %s", payload)

    # Простейшая MVP-логика: эхо-ответ, если есть текст
    text = None
    chat_id = None

    # Пример извлечения данных (структура зависит от реального BotX payload)
    # Подстройте под ваш формат входящих событий
    if isinstance(payload, dict):
        text = payload.get("text") or payload.get("body")
        chat_id = payload.get("chat_id") or payload.get("conversation_id")

    if text and chat_id:
        # Отправляем ответ в eXpress (заглушка/черновик)
        try:
            send_message_via_botx(chat_id, f"echo: {text}")
        except Exception:
            app.logger.exception("Failed to send BotX notification")

    # Протокол BotX ожидает 202 на приём команды
    return "", 202


def send_message_via_botx(chat_id: str, text: str) -> None:
    """
    Черновая отправка сообщения через BotX Notifications API.
    ВНИМАНИЕ: замените URL и поля на точные из вашей версии BotX API.
    Лучше в будущем перейти на официальную библиотеку pybotx.
    """
    if not (BOTX_BOT_ID and BOTX_SECRET and BOTX_CTS_URL):
        app.logger.warning("BOTX creds are not set; skip sending")
        return

    # Примерный endpoint (уточните по вашей версии BotX):
    # Ниже — безопасная заглушка: просто логируем.
    # Для реальной отправки раскомментируйте и подставьте верные пути/поля.

    app.logger.info("Would send to chat_id=%s: %s", chat_id, text)

    # Example (!!! адаптировать под ваш BotX !!!):
    # url = f"{BOTX_CTS_URL}/api/v3/botx/notifications"
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": f"Bearer {BOTX_SECRET}",  # если используется bearer
    # }
    # data = {
    #     "bot_id": BOTX_BOT_ID,
    #     "chat_id": chat_id,
    #     "body": {"text": text},
    # }
    # resp = requests.post(url, json=data, headers=headers, timeout=10)
    # resp.raise_for_status()
