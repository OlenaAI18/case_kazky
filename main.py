from flask import Flask, request
import requests
import random
import os

app = Flask(__name__)

# Казки (імпортуємо як словник stories)
from stories import stories

# Телеграм токен (додається в перемінні середовища VERCEL)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

# Сесії користувачів
user_sessions = {}

# Старт
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Початок
        if text == "/start":
            user_sessions[chat_id] = {}
            send_message(chat_id, "Привіт! 👋 Я бот Віталінки з чарівними казками. Для кого шукаємо історію?",
                         buttons=[["👧 Дівчинка"], ["👦 Хлопчик"]])

        elif text in ["👧 Дівчинка", "👦 Хлопчик"]:
            gender = "girl" if "Дівчинка" in text else "boy"
            user_sessions[chat_id] = {"gender": gender}
            send_message(chat_id, "Введи ім’я дитини:")

        elif chat_id in user_sessions and "gender" in user_sessions[chat_id] and "name" not in user_sessions[chat_id]:
            name = text.strip().capitalize()
            user_sessions[chat_id]["name"] = name
            story = random.choice(stories[user_sessions[chat_id]["gender"]])
            story_text = story["text"].replace("{{name}}", name)
            send_message(chat_id, f"📖 *{story['title']}*\n\n{story_text}", parse_mode="Markdown",
                         buttons=[["✨ Ще одну казку"]])

        elif text == "✨ Ще одну казку":
            if chat_id in user_sessions and "gender" in user_sessions[chat_id] and "name" in user_sessions[chat_id]:
                gender = user_sessions[chat_id]["gender"]
                name = user_sessions[chat_id]["name"]
                story = random.choice(stories[gender])
                story_text = story["text"].replace("{{name}}", name)
                send_message(chat_id, f"📖 *{story['title']}*\n\n{story_text}", parse_mode="Markdown",
                             buttons=[["✨ Ще одну казку"]])
            else:
                send_message(chat_id, "Щось пішло не так. Напиши /start, щоб почати спочатку.")

        else:
            send_message(chat_id, "Напиши /start, щоб розпочати ✨")

    return "ok"


def send_message(chat_id, text, buttons=None, parse_mode=None):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    if buttons:
        keyboard = {"keyboard": buttons, "resize_keyboard": True, "one_time_keyboard": False}
        payload["reply_markup"] = keyboard

    requests.post(API_URL + "sendMessage", json=payload)


if __name__ == "__main__":
    app.run(debug=True)
