from telegram import ReplyKeyboardMarkup

if update.message:
    chat_id = update.message.chat.id
    text = update.message.text.lower()

    if text in ["/start", "почати", "привіт"]:
        keyboard = [["Хочу казку"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        bot.send_message(chat_id=chat_id, text="Привіт! Я Віталінка. Хочеш казку?", reply_markup=reply_markup)

    elif text == "хочу казку":
        bot.send_message(chat_id=chat_id, text="Скажи, як звати дитину?")

    elif text.isalpha() and len(text) > 2:
        child_name = text.capitalize()
        fairy_tale = f"Жила-була дівчинка на ім’я {child_name}. Одного разу вона знайшла чарівний ліхтарик..."
        bot.send_message(chat_id=chat_id, text=fairy_tale)

    else:
        bot.send_message(chat_id=chat_id, text="Не зовсім зрозуміла. Натисни кнопку або введи ім'я дитини 💬")



