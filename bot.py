import telegram.ext as tg
from os import environ
import nse_utils

TOKEN = "2141022676:AAGrCeD0dlrWxs5irKLS4yRha_UwwGTZEQw"


# MESSAGE HANDLER
def handle_message(update, context):
    symbol = update.message.text
    response = nse_utils.get_price(symbol)
    update.message.reply_text(response)
    
# COMMANDS 
# /////////////// Testing purpose
def list(update, context):
    update.message.reply_text(nse_utils.INDEX_LIST)
# /////////////// 




# UPDATER & DISPATCHER
updater = tg.Updater(TOKEN)
dp = updater.dispatcher


# COMMANDS
dp.add_handler(tg.CommandHandler("list", list))

dp.add_handler(tg.MessageHandler(tg.Filters.text, handle_message))


PORT = int(environ.get('PORT', '8443'))

# updater.start_webhook(listen="0.0.0.0",
#                       port=PORT,
#                       url_path=TOKEN,
#                       webhook_url="https://naman-bot.herokuapp.com/" + TOKEN)


# POLLING
updater.start_polling()
print("Polling has started")