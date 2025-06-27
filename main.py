from fastapi import FastAPI, Request
import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from stories import girl_stories, boy_stories

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Зберігаємо дані користувача
user_data = {}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    print("📩 Update received:", data)  # Додаємо лог

    update = telegram.Update.de_json(data, bot)

    # Якщо прийшло звичайне повідомлення
    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text.strip() if update.message.text else ""

        print("🗨️ Text message:", text)

        # Старт
        if text and text.lower() == "/start":
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

        # Якщо вже обрали стать, просимо ім’я
        elif user_data.get(chat_id, {}).get("step") == "name":
            name = text
            user_data[chat_id]["name"] = name
            gender = user_data[chat_id]["gender"]
            user_data[chat_id]["story_index"] = 0

            stories = girl_stories if gender == "girl" else boy_stories
            story = stories[0].replace("{name}", name)
            keyboard = [[InlineKeyboardButton("📖 Розкажи ще", callback_data="more_story")]]
            bot.send_message(chat_id, story, reply_markup=InlineKeyboardMarkup(keyboard))

    # Якщо прийшов клік на кнопку
    elif update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat.id
        data = query.data

        print("🔘 Callback:", data)

        # Обрали стать
        if data in ["girl", "boy"]:
            user_data[chat_id] = {"gender": data, "step": "name"}
            prompt = "А як звати нашу зірочку? ✨" if data == "girl" else "А як звати нашого героя? ✨"
            bot.send_message(chat_id, prompt)

        # Обрали "ще одну казку"
        elif data == "more_story":
            user_info = user_data.get(chat_id)
            if not user_info or "name" not in user_info:
                bot.send_message(chat_id, "Натисніть /start, щоб почати заново.")
                return {"ok": True}

            gender = user_info["gender"]
            name = user_info["name"]
            stories = girl_stories if gender == "girl" else boy_stories
            idx = user_info.get("story_index", 0) + 1

            if idx >= len(stories):
                idx = 0  # якщо історії закінчились — починаємо спочатку

            user_info["story_index"] = idx
            story = stories[idx].replace("{name}", name)
            keyboard = [[InlineKeyboardButton("📖 Розкажи ще", callback_data="more_story")]]
            bot.send_message(chat_id, story, reply_markup=InlineKeyboardMarkup(keyboard))

    return {"ok": True}







