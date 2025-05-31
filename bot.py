from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Application

# Токен, полученный от BotFather
TOKEN = "YOUR_BOT_TOKEN"

# Список для отслеживания сообщений пользователей
user_message_count = {}

MAX_STICKERS = 5

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я антиспам-бот.")

async def check_spam(update: Update, context):
    user_id = update.message.from_user.id
    if user_id not in user_message_count:
        user_message_count[user_id] = 0

    if update.message.sticker:
        user_message_count[user_id] += 1
        if user_message_count[user_id] > MAX_STICKERS:
            await update.message.reply_text("Вы превысили лимит стикеров! Мьют.")
            await context.bot.restrict_chat_member(update.message.chat.id, user_id, can_send_messages=False)
        else:
            await update.message.reply_text(f"Вы отправили {user_message_count[user_id]} стикеров. Лимит: {MAX_STICKERS}")

    elif update.message.text:
        pass

async def unmute(update: Update, context):
    user_id = update.message.from_user.id
    await context.bot.restrict_chat_member(update.message.chat.id, user_id, can_send_messages=True)
    await update.message.reply_text("Вы размьючены!")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("unmute", unmute))
    application.add_handler(MessageHandler(Filters.text | Filters.sticker, check_spam))

    application.run_polling()

if __name__ == '__main__':
    main()
