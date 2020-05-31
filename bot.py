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
            "googlesg", self.subscribe_to_google_sg))
        self.dp.add_handler(CommandHandler(
            "googleus", self.subscribe_to_google_us))
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

    # subscribe to receive trending google singapore searches every 30 mins
    def subscribe_to_google_sg(self, update, context):
        self.id = update.effective_chat.id
        self.updater.job_queue.run_repeating(
            self.google_trending_sg, interval=3600, first=0)

    # subscribe to receive trending google USA searches every 45 mins
    def subscribe_to_google_us(self, update, context):
        self.id = update.effective_chat.id
        self.updater.job_queue.run_repeating(
            self.google_trending_us, interval=2700, first=0)

    def google_trending_us(self, context: telegram.ext.CallbackContext):
        channel_posted_array = [0]
        # get feed
        gfeed = GoogleTrendingSearch('US')
        # get today uses local time. Need to change to US time
        gfeed.get_feed_data_all()

        # file io
        try:
            f = open("us.p", "rb")
            channel_posted_array = pickle.load(f)
            f.close()
        except:
            f = open("us.p", 'wb')
            pickle.dump(channel_posted_array, f)
            f.close()

        f.close()

        for item in gfeed.feed_array:
            if hash(item) not in channel_posted_array:
                channel_posted_array.append(hash(item))
                f = open("us.p", "wb")
                pickle.dump(channel_posted_array, f)
                f.close()
                context.bot.send_photo(chat_id=self.id, photo=self.google_trending_search_image,
                                       caption=item.formatted_lite_us(), disable_notification=True)
                break

    def google_trending_sg(self, context: telegram.ext.CallbackContext):
        posted_array = [0]
        # get feed
        gfeed = GoogleTrendingSearch('SG')
        gfeed.get_feed_data_today()
        # file io
        try:
            f = open("sg.p", "rb")
            posted_array = pickle.load(f)
            f.close()
        except:
            f = open("sg.p", 'wb')
            pickle.dump(posted_array, f)
            f.close()
        f.close()

        for item in gfeed.feed_array:
            if hash(item) not in posted_array:
                # write to file instead of local variable
                posted_array.append(hash(item))
                f = open("sg.p", "wb")
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
                context.bot.send_photo(chat_id=update.effective_chat.id,
                                       photo=self.google_trending_search_image, caption=item.formatted(), parse_mode=telegram.ParseMode.HTML)
                break

    def cleaner(self):
        schedule.every().day.at("00:00").do(self.clean)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def clean(self):
        os.remove('sg.p')
