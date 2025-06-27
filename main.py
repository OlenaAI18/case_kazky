from fastapi import FastAPI, Request
import os
import telegram

app = FastAPI()

# Отримуємо токен
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Простий стан користувачів
user_state = {}  # chat_id -> {"step": ..., "name": ..., "gender": ...}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def receive_update(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, bot)

    if not update.message:
        return {"ok": True}

    chat_id = update.message.chat.id
    text = update.message.text.strip()

    if chat_id not in user_state:
        user_state[chat_id] = {"step": "start"}

    step = user_state[chat_id]["step"]

    # Початок
    if text == "/start" or step == "start":
        bot.send_message(chat_id=chat_id, text="Привіт! Я твій казковий помічник ✨\nЯк тебе звати?")
        user_state[chat_id]["step"] = "ask_name"
        return {"ok": True}

    # Крок 1: ім'я
    if step == "ask_name":
        user_state[chat_id]["name"] = text
        bot.send_message(chat_id=chat_id, text="Чудово, " + text + "! А яка у тебе стать? (хлопчик / дівчинка)")
        user_state[chat_id]["step"] = "ask_gender"
        return {"ok": True}

    # Крок 2: стать
    if step == "ask_gender":
        gender = text.lower()
        if gender not in ["хлопчик", "дівчинка"]:
            bot.send_message(chat_id=chat_id, text="Вибач, я зрозумію тільки 'хлопчик' або 'дівчинка'.")
            return {"ok": True}

        user_state[chat_id]["gender"] = gender
        name = user_state[chat_id]["name"]

        # Казка
        fairy_tale = f"Одного разу {gender} на ім'я {name} вирушив у чарівну пригоду... 🌈🦄"

        bot.send_message(chat_id=chat_id, text=fairy_tale)
        user_state[chat_id]["step"] = "done"
        return {"ok": True}

    # Повторне натискання після завершення
    if step == "done":
        bot.send_message(chat_id=chat_id, text="Хочеш ще раз? Напиши /start")
        return {"ok": True}

    return {"ok": True}





