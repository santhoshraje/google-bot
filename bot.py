# telegram modules
from telegram.ext import Updater, CommandHandler
import telegram.ext
# system modules
import os
from threading import Thread
import time
# pip modules
import schedule
# custom modules
from config_loader import get_config_value as load
from google_feed import GoogleFeed

class Bot:
    def __init__(self, config):
        # loaded from config
        self.token = load(config, 'BOT_TOKEN')
        self.channel_id = load(config, 'CHANNEL_ID')
        self.google_trending_search_image = load(
            config, 'GOOGLE_TRENDING_IMAGE')
        # telegram api
        self.updater = Updater(self.token, use_context=True)
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher
        # bot commands
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler(
            "trending", self.subscribe_to_google))
        # self.dp.add_handler(CommandHandler(
        #     "testfeed", self.google_trending_testing))
        # variables used by bot
        self.id = 0

    def start_bot(self):
        print('bot active')
        Thread(target=self.cleanup).start()
        self.updater.start_polling()

    def start(self, update, context):
        self.id = update.effective_chat.id
        context.bot.send_message(chat_id=self.id,
                                 text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.',
                                 parse_mode=telegram.ParseMode.HTML)

    # subscribe to receive trending google singapore searches every 60 mins
    def subscribe_to_google(self, update, context):
        self.id = update.effective_chat.id
        self.updater.job_queue.run_repeating(
            self.trending, interval=3600, first=0)

    # testing for individual functions
    def trending(self, context):
        item = GoogleFeed().get_item()
        if item:
            context.bot.send_photo(chat_id=self.id,
                                   photo=self.google_trending_search_image, caption=item.formatted(), parse_mode=telegram.ParseMode.HTML)

    def cleanup(self):
        schedule.every().day.at("00:00").do(self.purge)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def purge(self):
        os.remove('trending.pickle')
