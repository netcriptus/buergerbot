import os
from time import sleep
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()
token = os.getenv('TOKEN')

SELECT_SERVICE, ANMELDUNG = range(2)
AVAILABLE_SERVICES = ["Anmeldung"]

SERVICE_RUNNING = False

async def start(update, _):
    print(f'At start service. Received {update.message.text}')
    reply_keyboard = [AVAILABLE_SERVICES]
    await update.message.reply_text(
        'Hello, welcome to your Berlin assistant Bot!',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    print('exiting start')
    return SELECT_SERVICE

async def anmeldung(update, _):
    print(f'At anmeldung. Received {update.message.text}')
    while SERVICE_RUNNING:
        await update.message.reply_text("Anmeldung erfolgreich!", reply_markup=ReplyKeyboardMarkup([['Stop']]))
        sleep(10)
    print('exiting anmeldung')
    return ConversationHandler.END

async def start_service(update, _):
    print(f'At start_service. Received {update.message.text}')
    global SERVICE_RUNNING
    selected_service = update.message.text
    if selected_service not in AVAILABLE_SERVICES:
        reply_keyboard = [AVAILABLE_SERVICES]
        await update.message.reply_text(
            "Sorry, I don't know this service. Please select one of the following services:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return SELECT_SERVICE
    SERVICE_RUNNING = True
    print('exiting start_service')
    return ANMELDUNG

async def stop_service(update, _):
    print(f'At stop_service. Received {update.message.text}')
    global SERVICE_RUNNING
    SERVICE_RUNNING = False
    await update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove(),)
    print('exiting stop_service')
    return ConversationHandler.END

def main():
    application = Application.builder().token(token).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_SERVICE: [MessageHandler(filters.Regex('^[' + '|'.join(AVAILABLE_SERVICES) + ']$'), start_service)],
            ANMELDUNG: [MessageHandler('Anmeldung', anmeldung), CommandHandler("Stop", stop_service)]
        },
        fallbacks=[CommandHandler("stop", stop_service)]
    )

    application.add_handler(conversation_handler)
    print('Bot is running...')
    application.run_polling()


if __name__ == '__main__':
    main()
