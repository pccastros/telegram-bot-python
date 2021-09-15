from telegram import ParseMode

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
