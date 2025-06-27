from fastapi import FastAPI, Request
import os
import telegram
from telegram import ReplyKeyboardMarkup
import random

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Фейкові казки
stories = {
    "girl": [
        {"title": "Казка про зірку", "text": "Жила-була дівчинка на ім’я {{name}}, яка знайшла чарівну зірку..."},
        {"title": "Казка про ліс", "text": "{{name}} пішла до лісу, де всі тваринки заговорили з нею..."}
    ],
    "boy": [
        {"title": "Казка про дракона", "text": "Хлопчик {{name}} зустрів доброго дракона, який вмів літати..."},
        {"title": "Казка про машинку", "text": "{{name}} знайшов чарівну машинку, що вміла говорити..."}
    ]
}

user_sessions = {}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def receive_update(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text.strip()

        session = user_sessions.get(chat_id, {})

        if text == "/start" or not session:
            user_sessions[chat_id] = {}
            reply_markup = ReplyKeyboardMarkup([["👧 Дівчинка"], ["👦 Хлопчик"]], resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text="Привіт! 👋 Я бот "Казки" з чарівними казками. Для кого шукаємо історію?", reply_markup=reply_markup)

        elif text in ["👧 Дівчинка", "👦 Хлопчик"]:
            gender = "girl" if "Дівчинка" in text else "boy"
            user_sessions[chat_id] = {"gender": gender}
            bot.send_message(chat_id=chat_id, text="Введи ім’я дитини:")

        elif "gender" in session and "name" not in session:
            name = text.capitalize()
            user_sessions[chat_id]["name"] = name
            gender = session["gender"]
            story = random.choice(stories[gender])
            story_text = story["text"].replace("{{name}}", name)
            reply_markup = ReplyKeyboardMarkup([["✨ Ще одну казку"]], resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=f"📖 *{story['title']}*\n\n{story_text}", parse_mode="Markdown", reply_markup=reply_markup)

        elif text == "✨ Ще одну казку" and "gender" in session and "name" in session:
            gender = session["gender"]
            name = session["name"]
            story = random.choice(stories[gender])
            story_text = story["text"].replace("{{name}}", name)
            bot.send_message(chat_id=chat_id, text=f"📖 *{story['title']}*\n\n{story_text}", parse_mode="Markdown")

        else:
            bot.send_message(chat_id=chat_id, text="Напиши /start, щоб розпочати ✨")

    return {"ok": True}




