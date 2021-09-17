from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import ConversationHandler, CallbackContext
from utils import sendMessage, sendMessageInline, createCalendar, calendarInline
from math import sin, cos, atan2, sqrt

# states
NAME, CITY, DISTANCE, LOCATION, DATE = range(100, 105)


# start function
def start(update: Update, context: CallbackContext) -> int:
    message = "Send me a command to start:\n\n/hello - Start conversation"
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# end function
def end(update: Update, context: CallbackContext) -> int:
    message = 'Time Out!'
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    message = "Send me a command to start:\n\n/hello - Start conversation"
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def hello(update: Update, context: CallbackContext) -> int:
    message_out = "Hi, I'm Lucy, your travel assistant, what's your name?"
    sendMessage(update=update, context=context, message=message_out, keyboard=ReplyKeyboardRemove())
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


def distance(update: Update, context: CallbackContext) -> int:

    text = update.message.text.lower()

    if 'yes' in text.lower():
        location_keyboard = KeyboardButton(text="Send my location \U0001F4CD",  request_location=True)
        custom_keyboard = [[ location_keyboard ]]
        markup = ReplyKeyboardMarkup(custom_keyboard) 
        message_out = 'Please send me your location'
        sendMessage(update=update, context=context, message=message_out, keyboard=markup)
        return LOCATION

    elif 'no' in text.lower():
        message_out = 'Choose a tentative date'
        sendMessage(update=update, context=context, message=message_out, keyboard=createCalendar())
        return DATE

    else:
        city = context.user_data['city']
        message_out = f'Would you like to know how far {city} is from you?'
        reply_keyboard = [['\U00002705  Yes', '\U0000274C  No']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=False)
        sendMessageInline(update=update, context=context, message=message_out, keyboard=markup)
        return DISTANCE


def location(update: Update, context: CallbackContext) -> int:

    if update.message.location:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        print(lat, lon)

        if context.user_data['city'] == 'New York' : 
            lat_city = 40.7815955 
            lon_city = -73.9830113

        elif context.user_data['city'] == 'Tokio' : 
            lat_city = 35.6684415
            lon_city = 139.6007841

        elif context.user_data['city'] == 'Istanbul' : 
            lat_city = 41.0054958
            lon_city = 28.8720963

        # calcule distance between coords
        dist_lon = lon_city - lon
        dist_lat = lat_city - lat

        a = sin(dist_lat / 2)**2 + cos(lat) * cos(lat_city) * sin(dist_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = int(6373.0 * c)

        message_out = f'You are located *{distance}km* away'
        sendMessage(update=update, context=context, message=message_out, keyboard=ReplyKeyboardRemove())

        message_out = 'Choose a tentative date'
        sendMessage(update=update, context=context, message=message_out, keyboard=createCalendar())
        return DATE

    else:
        location_keyboard = KeyboardButton(text="Send my location \U0001F4CD",  request_location=True)
        custom_keyboard = [[ location_keyboard ]]
        markup = ReplyKeyboardMarkup(custom_keyboard) 
        message_out = 'Please send me your location.'
        sendMessage(update=update, context=context, message=message_out, keyboard=markup)
        return LOCATION


def date(update, context) -> int:

    bot = context.bot
    _, date = calendarInline(bot, update)
    
    message_out = "Travel date: " + (date.strftime("%d/%m/%Y"))

    sendMessageInline(update=update, context=context, message=message_out, keyboard=None)

    name = context.user_data['name']
    message_out = f"{name}, the tour could cost $ 5200"
    sendMessageInline(update=update, context=context, message=message_out, keyboard=None)

    message_out = "Thanks, an advisor will contact you. Send /hello to start a new conversation."
    sendMessageInline(update=update, context=context, message=message_out, keyboard=None)

    message_out = "Have a nice day!!"
    sendMessageInline(update=update, context=context, message=message_out, keyboard=None)

    return ConversationHandler.END