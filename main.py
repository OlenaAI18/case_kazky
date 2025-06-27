from fastapi import FastAPI, Request
import os
import telegram
from telegram import ReplyKeyboardMarkup
from stories import get_story

app = FastAPI()

# Бот Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Тимчасове зберігання даних користувача
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

        # Якщо користувач ще не вибрав стать
        if chat_id not in user_data:
            reply_markup = ReplyKeyboardMarkup([["👦 Хлопчик", "👧 Дівчинка"]], resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text="Хто слухатиме казку? 🌟", reply_markup=reply_markup)
            user_data[chat_id] = {}
            return {"ok": True}

        # Вибір статі
        if "gender" not in user_data[chat_id]:
            if "хлопчик" in text.lower():
                user_data[chat_id]["gender"] = "male"
            elif "дівчинка" in text.lower():
                user_data[chat_id]["gender"] = "female"
            else:
                bot.send_message(chat_id=chat_id, text="Будь ласка, обери: 👦 Хлопчик або 👧 Дівчинка")
                return {"ok": True}

            bot.send_message(chat_id=chat_id, text="А як звати нашу зірочку? ✨")
            return {"ok": True}

        # Запис імені та генерація казки
        if "name" not in user_data[chat_id]:
            user_data[chat_i_]()_






