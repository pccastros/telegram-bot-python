from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from states import *
import logging


# logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# api token
API_TOKEN = 'HERE YOUR API-TOKEN'

# states
NAME, CITY, DISTANCE, LOCATION, DATE = range(100, 105)


def main() -> None:

    # updater and dispatcher
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    # conversarion Handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('hi', hello),
            CommandHandler('hello', hello)
        ],
        states={
            NAME: [ MessageHandler(Filters.chat_type.private, name)],
            CITY: [ 
                MessageHandler(Filters.chat_type.private, selectCity),
                CallbackQueryHandler(selectCityInline)
            ],
            DISTANCE: [ MessageHandler(Filters.chat_type.private, distance)],
            LOCATION: [ MessageHandler(Filters.chat_type.private, location)],
            DATE: [CallbackQueryHandler(date)]
        },
        fallbacks=[
            CommandHandler('exit', end),
        ],

        # Timeout session
        conversation_timeout=60
    )


    # add conversation handler
    dispatcher.add_handler(conv_handler)

    # for unknown text or commands
    dispatcher.add_handler(MessageHandler(Filters.text & (~ Filters.command), start))
    dispatcher.add_handler(MessageHandler(Filters.command, start))

    # start bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()