from fastapi import FastAPI, Request
import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from stories import get_story

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Зберігаємо сесії користувачів
user_data = {}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    print("📩 Update received:", data)

    update = telegram.Update.de_json(data, bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text.strip() if update.message.text else ""

        if text.lower() == "/start":
            user_data[chat_id] = {"step": "gender"}
            keyboard = [
                [InlineKeyboardButton("👧 Дівчинка", callback_data="girl")],
                [InlineKeyboardButton("👦 Хлопчик", callback_data="boy")]
            ]
            bot.send_message(
                chat_id,
                "Привіт! Я твій AI-казкар від бренду Х 📚✨\n\nХто слухатиме сьогоднішню історію?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif user_data.get(chat_id, {}).get("step") == "name":
            name = text
            gender = user_data[chat_id]["gender"]
            story = get_story(name, gender)

            user_data[chat_id]["name"] = name
            user_data[chat_id]["step"] = "done"

            keyboard = [[InlineKeyboardButton("📖 Розкажи ще", callback_data="more_story")]]
            bot.send_message(chat_id, story, reply_markup=InlineKeyboardMarkup(keyboard))

    elif update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat.id
        data = query.data

        if data in ["girl", "boy"]:
            gender = "female" if data == "girl" else "male"
            user_data[chat_id] = {"gender": gender, "step": "name"}
            bot.send_message(chat_id, "Як звати дитину?")

        elif data == "more_story":
            user = user_data.get(chat_id)
            if user and "name" in user and "gender" in user:
                story = get_story(user["name"], user["gender"])
                keyboard = [[InlineKeyboardButton("📖 Розкажи ще", callback_data="more_story")]]
                bot.send_message(chat_id, story, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                bot.send_message(chat_id, "Напиши /start, щоб почати знову.")

    return {"ok": True}







