from telegram.ext import Updater, CommandHandler
import telegram.ext
from config_loader import get_config_value as load
from trending_searches_rss import GoogleTrendingSearch
import pickle
import os
from threading import Thread
import schedule
import time

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
        self.dp.add_handler(CommandHandler(
            "testfeed", self.google_trending_testing))
        # variables used by bot
        self.id = 0

    def start_bot(self):
        print('bot active')
        Thread(target=self.cleaner).start()
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
            self.google_trending, interval=3600, first=0)

    # renamed from google_trending_sg
    def google_trending(self, context):
        posted_array = [0]
        # get feed
        gfeed = GoogleTrendingSearch('SG')
        gfeed.get_feed_data_today()
        # file io
        try:
            f = open("trending.p", "rb")
            posted_array = pickle.load(f)
            f.close()
        except:
            f = open("trending.p", 'wb')
            pickle.dump(posted_array, f)
            f.close()
        f.close()

        for item in gfeed.feed_array:
            if hash(item) not in posted_array:
                # write to file instead of local variable
                posted_array.append(hash(item))
                f = open("trending.p", "wb")
                pickle.dump(posted_array, f)
                f.close()
                context.bot.send_photo(
                    chat_id=self.id, photo=self.google_trending_search_image, caption=item.formatted_lite())
                break

    # testing for individual functions
    def google_trending_testing(self, update, context):
        posted_array = [0]
        # get feed
        gfeed = GoogleTrendingSearch('SG')
        gfeed.get_feed_data_today()
        # file io
        try:
            f = open("test.p", "rb")
            posted_array = pickle.load(f)
            f.close()
        except:
            f = open("test.p", 'wb')
            pickle.dump(posted_array, f)
            f.close()

        f.close()

        for item in gfeed.feed_array:
            if hash(item) not in posted_array:
                # write to file instead of local variable
                posted_array.append(hash(item))
                print(item)
                print(hash(item))
                f = open("test.p", "wb")
                pickle.dump(posted_array, f)
                f.close()
                context.bot.send_photo(chat_id = update.effective_chat.id,
                                       photo=self.google_trending_search_image, caption=item.formatted(), parse_mode=telegram.ParseMode.HTML)
                break

    def cleaner(self):
        schedule.every().day.at("00:00").do(self.clean)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def clean(self):
        os.remove('trending.p')