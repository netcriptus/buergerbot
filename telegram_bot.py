import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

load_dotenv()

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

token = os.getenv('TOKEN')
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
