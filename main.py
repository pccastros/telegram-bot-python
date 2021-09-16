from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from states import *
import logging


# logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# api token
API_TOKEN = '1780879310:AAH5xxQYja5HtefAwzOEdOXQVpi0O6Br1DI'

# states
NAME, CITY, DISTANCE, LOCATION, DATE = range(100, 105)


def main() -> None:

    # Updater and Dispatcher
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    ############################################################################
    ## FLUJO PAGO CAJERO
    ############################################################################
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
            #MessageHandler(Filters.chat_type.private, errorSesion)
        ],
        conversation_timeout=60
    )


    ## Agregar Flujos
    dispatcher.add_handler(conv_handler)

    ## Handler general: palabras y comandos desconocidos
    dispatcher.add_handler(MessageHandler(Filters.text & (~ Filters.command), start))
    dispatcher.add_handler(MessageHandler(Filters.command, start))

    # Iniciar Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()