from fastapi import FastAPI, Request
import os
import telegram

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def receive_update(request: Request):
    try:
        data = await request.json()
        update = telegram.Update.de_json(data, bot)

        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text
            bot.send_message(chat_id=chat_id, text="Привіт! Я працюю 👋")

        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


