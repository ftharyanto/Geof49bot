from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
    ForceReply, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
    Filters, RegexHandler, ConversationHandler)
import logging, re

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

USER_TEXT = 0

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hai! saya Geofisika 49 bot!')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Tolong dong!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s membatalkan konversi.", user.first_name)
    update.message.reply_text('Konversi dibatalkan.',
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def konvert(bot, update):
    user = update.message.from_user
    logger.info("User %s mengkonversi", user.first_name)
    update.message.reply_text('silakan masukkan teks yang ingin dikonversi, /cancel untuk membatalkan',
       reply_markup = ForceReply(selective=True))
    return USER_TEXT

def balas(bot, update):
    teks = update.message.text
    user = update.message.from_user

    logger.info("Teks user %s: %s", user.first_name, teks)
    rep = {"*": "**", "_": "__"} # define desired replacements here

    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    replyMessage = pattern.sub(lambda m: rep[re.escape(m.group(0))], teks)

    update.message.reply_text(replyMessage, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("xxxxxxxxxxxxxxxxxxxxxxxx")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states USER_TEXT
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('konvert', konvert)],

        states={
            USER_TEXT: [MessageHandler(Filters.text, balas)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(conv_handler)


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
