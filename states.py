from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext
from utils import sendMessage, sendMessageInline

# states
NAME, CITY, DISTANCE, LOCATION, DATE = range(100, 105)

# start function
def start(update: Update, context: CallbackContext) -> int:
    message = "Send me a command to start:\n\n/hi:\n/hello:"
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove(),)
    return ConversationHandler.END

# end function
def end(update: Update, context: CallbackContext) -> int:
    message = 'Time Out!'
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    message = "Send me a command to start:\n\n/hi:\n/hello:"
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def hello(update: Update, context: CallbackContext) -> int:
    message_out = "Hi, I'm Lucy, your travel assistant, what's your name?"
    sendMessage(update=update, context=context, message=message_out, keyboard=None)
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    mensaje_in = update.message.text
    context.user_data['name'] =  mensaje_in
    message_out = f'Nice to meet you {mensaje_in}, please select the city you want to visit.'
    menu = [
        [ InlineKeyboardButton("\U0001F5FD  New York", callback_data="New York")],
        [ InlineKeyboardButton("\U000026E9  Tokio", callback_data="Tokio")],
        [ InlineKeyboardButton("\U0001F54C  Istanbul", callback_data="Istanbul")],
    ]
    markup = InlineKeyboardMarkup(menu)
    sendMessage(update=update, context=context, message=message_out, keyboard=markup)
    return CITY


def selectCity(update: Update, context: CallbackContext) -> int:
    message_out = 'Hello, please select the city you want to visit.'
    menu = [
        [ InlineKeyboardButton("\U0001F5FD  New York", callback_data="New York")],
        [ InlineKeyboardButton("\U000026E9  Tokio", callback_data="Tokio")],
        [ InlineKeyboardButton("\U0001F54C  Istanbul", callback_data="Istanbul")],
    ]
    markup = InlineKeyboardMarkup(menu)
    sendMessage(update=update, context=context, message=message_out, keyboard=markup)
    return DISTANCE


def selectCityInline(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    city = query.data
    context.user_data['city'] =  city

    message_out = f'You have selected: {city}'
    query.edit_message_text(text=message_out, parse_mode=ParseMode.MARKDOWN)
    
    message_out = f'Would you like to know how far {city} is from you?'
    reply_keyboard = [['\U00002705  Yes', '\U0000274C  No']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=False)
    sendMessageInline(update=update, context=context, message=message_out, keyboard=markup)
    return DISTANCE



def selectDistance(update: Update, context: CallbackContext) -> int:
    
    message_out = 'Hello, please select the city you want to visit.'
    menu = [
        [ InlineKeyboardButton("\U0001F5FD  New York", callback_data="New York")],
        [ InlineKeyboardButton("\U000026E9  Tokio", callback_data="Tokio")],
        [ InlineKeyboardButton("\U0001F54C  Istanbul", callback_data="Istanbul")],
    ]
    markup = InlineKeyboardMarkup(menu)

    sendMessage(update=update, context=context, message=message_out, keyboard=markup)
    return 2