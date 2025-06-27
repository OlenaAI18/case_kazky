from fastapi import FastAPI, Request
import os
import telegram
from telegram import ReplyKeyboardMarkup
from stories import get_story

app = FastAPI()

# Ініціалізація бота
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Памʼять користувачів
user_data = {}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def receive_update(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text
        user = user_data.get(chat_id, {})

        if text == "/start":
            bot.send_message(
                chat_id=chat_id,
                text="Привіт! Я твій АІ-казкар від бренду Х. 🧚‍♀️\nГотовий створити для тебе чарівну історію! Спочатку скажи, хто ти:",
                reply_markup=ReplyKeyboardMarkup(
                    [["👧 Дівчинка", "🧒 Хлопчик"]],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
            )
            user_data[chat_id] = {}  # Скидаємо на нову сесію

        elif text in ["👧 Дівчинка", "🧒 Хлопчик"]:
            gender = "female" if "Дівчинка" in text else "male"
            user["gender"] = gender
            user_data[chat_id] = user
            bot.send_message(chat_id=chat_id, text="А як звати нашу зірочку? ✨")

        elif "gender" in user and "name" not in user:
            name = text.strip()
            user["name"] = name
            user_data[chat_id] = user
            story = get_story(name, user["gender"])
            bot.send_message(chat_id=chat_id, text=story, reply_markup=ReplyKeyboardMarkup(
                [["✨ Розкажи ще"]],
                resize_keyboard=True
            ))

        elif text == "✨ Розкажи ще":
            if "name" in user and "gender" in user:
                story = get_story(user["name"], user["gender"])
                bot.send_message(chat_id=chat_id, text=story)

        else:
            bot.send_message(chat_id=chat_id, text="Натисни /start, щоб почати заново 🌀")

    return {"ok": True}






