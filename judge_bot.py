import random
from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен вашего бота
TOKEN = 7839012993:AAHxueEGDLQJDjzeW_p-0C_3f7cHdctf3Vw

# Меры пресечения и их вероятности
PUNISHMENTS = [
    {"name": "Расстрел", "action": "ban", "duration": 1 * 24 * 60 * 60, "probability": 0.6},  # 60%
    {"name": "Кастрация", "action": "mute", "duration": 3 * 60 * 60, "probability": 0.39},  # 39%
    {"name": "Тебе пизда, ебанат", "action": "ban", "duration": 7 * 24 * 60 * 60, "probability": 0.01},  # 1%
]

def punish_user(update: Update, context: CallbackContext):
    # Проверяем, что команда вызвана в ответ на сообщение
    if not update.message.reply_to_message:
        update.message.reply_text("Ответь на сообщение, чтобы наказать человека!")
        return

    # Проверяем, что команда начинается с одного из префиксов
    command = update.message.text.lower()
    if not (command.startswith('!хуйня') or command.startswith('.хуйня') or command.startswith('/хуйня')):
        return  # Игнорируем, если префикс не совпадает

    # Выбираем меру пресечения
    punishment = random.choices(
        PUNISHMENTS,
        weights=[p["probability"] for p in PUNISHMENTS],
        k=1
    )[0]

    # Получаем ID пользователя, которого нужно наказать
    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.message.chat_id

    # Применяем меру пресечения
    if punishment["action"] == "ban":
        context.bot.ban_chat_member(chat_id, user_id, until_date=punishment["duration"])
    elif punishment["action"] == "mute":
        context.bot.restrict_chat_member(
            chat_id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=punishment["duration"]
        )

    # Отправляем сообщение о наказании
    update.message.reply_text(f"{punishment['name']}!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчик сообщений с командой "хуйня"
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, punish_user))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
