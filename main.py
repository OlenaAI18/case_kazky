from fastapi import FastAPI, Request
import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

user_data = {}  # user_id -> {"gender": "", "name": ""}

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

        if text == "/start":
            keyboard = [
                [InlineKeyboardButton("👦 Хлопчик", callback_data='male')],
                [InlineKeyboardButton("👧 Дівчинка", callback_data='female')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=chat_id, text="Хто буде головним героєм казки?", reply_markup=reply_markup)
            user_data[chat_id] = {}  # ініціалізуємо пустий словник
        elif chat_id in user_data and "gender" in user_data[chat_id] and "name" not in user_data[chat_id]:
            user_data[chat_id]["name"] = text
            gender = user_data[chat_id]["gender"]
            name = user_data[chat_id]["name"]

            # 👉 Тут можна вставити генерацію з GPT або шаблон
            fairy_tale = f"Жив-був {name}, маленький {'хлопчик' if gender == 'male' else 'дівчинка'}, який мріяв змінити світ... 🌟"
            bot.send_message(chat_id=chat_id, text=fairy_tale)

    elif update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat.id
        gender = query.data

        if chat_id not in user_data:
            user_data[chat_id] = {}

        user_data[chat_id]["gender"] = gender
        bot.send_message(chat_id=chat_id, text="А як звати нашу зірочку? ✨")

    return {"ok": True}





