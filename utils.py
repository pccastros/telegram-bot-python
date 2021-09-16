from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar

def sendMessage(update, context, message, keyboard=None):
    id_telegram = (update.message.from_user)['id']
    bot = context.bot
    if keyboard is None:
        bot.send_message(chat_id=id_telegram, text=message, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=id_telegram, text=message,
                         parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


def sendMessageInline(update, context, message, keyboard=None):
    id_telegram = update.callback_query.message.chat.id
    bot = context.bot
    if keyboard is None:
        bot.send_message(chat_id=id_telegram, text=message, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat_id=id_telegram, text=message,
                         parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


def createCalendar(year=None, month=None):

    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = ";".join(["IGNORE", str(year), str(month), str(0)])
    keyboard = []

    # first row: month and yead
    row = []
    row.append( InlineKeyboardButton(calendar.month_name[month] + " " +str(year) , callback_data=data_ignore))
    keyboard.append(row)

    # second row: day
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=";".join(["DAY", str(year), str(month), str(day)])))
        keyboard.append(row)

    # third row: buttons
    row=[]
    row.append( InlineKeyboardButton("<", callback_data=";".join(["PREV-MONTH", str(year), str(month), str(day)])))
    row.append( InlineKeyboardButton(">", callback_data=";".join(["NEXT-MONTH", str(year), str(month), str(day)])))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def calendarInline(bot, update):

    ret_data = (False,None)
    query = update.callback_query
    (action, year, month, day) = query.data.split(";")

    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id= query.id)

    elif action == "DAY":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True, datetime.datetime(int(year),int(month),int(day))

    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=createCalendar(int(pre.year),int(pre.month)))

    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=createCalendar(int(ne.year),int(ne.month)))

    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")

    return ret_data