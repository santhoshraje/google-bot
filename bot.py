  #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple telegram bot framework
"""
import logging

from telegram.ext import Updater, CommandHandler

# Command handler
def start(update, context):
    update.message.reply_text('Welcome to my Bot!')

def main():
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()