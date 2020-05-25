from telegram.ext import Updater, CommandHandler
from config_loader import get_config_value as load
from trending_searches_rss import GoogleTrendingSearch
import pickle
import os

class Bot:
    def __init__(self):
        self.token = load('BOT_TOKEN')        
        self.channel_id = load('CHANNEL_ID')
        # telegram api
        self.updater = Updater(self.token, use_context=True)
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher   
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("feed", self.google_trending_sg))
        self.dp.add_handler(CommandHandler("channel", self.google_trending_us))
        # variables
        self.image_url = 'https://miro.medium.com/max/821/1*Fi6masemXJT3Q8YWekQCDQ.png'


    def start_bot(self):
        print('bot active')
        self.updater.start_polling()
    
    def start(self, update, context):
        context.bot.send_message(chat_id= update.effective_chat.id, text="I'm a bot, please talk to me!") 
    
    def google_trending_sg(self, update, context):
        feed_url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG'
        posted_array = [0]

        # get feed
        gfeed = GoogleTrendingSearch(feed_url)
        gfeed.get_feed_data_today()

        # file io
        try:
            f = open("file.p", "rb")
            posted_array = pickle.load(f)
            f.close()
        except:
            f = open("file.p", 'wb')
            pickle.dump(posted_array, f)
            f.close()

        f.close()

        for item in gfeed.feed_array:
            if item.id not in posted_array:
                # write to file instead of local variable
                posted_array.append(item.id)
                f = open("file.p", "wb")
                pickle.dump(posted_array, f)
                f.close()
                context.bot.send_photo(chat_id = update.effective_chat.id, photo = self.image_url, caption = item.formatted_beta())
                break

    
    def google_trending_us(self, update, context):
        feed_url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=US'
        channel_posted_array = [0]
        # get feed
        gfeed = GoogleTrendingSearch(feed_url)
        gfeed.get_feed_data_all()

        # file io
        try:
            f = open("channel.p", "rb")
            channel_posted_array = pickle.load(f)
            f.close()
        except:
            f = open("channel.p", 'wb')
            pickle.dump(channel_posted_array, f)
            f.close()

        f.close()

        for item in gfeed.feed_array:
            if item.id not in channel_posted_array:
                channel_posted_array.append(item.id)
                f = open("channel.p", "wb")
                pickle.dump(channel_posted_array, f)
                f.close()                
                context.bot.send_photo(chat_id = self.channel_id, photo = self.image_url, caption = item.formatted_beta_us(), disable_notification = True)
                break

    
def test():
    posted_array = [0]
    feed_url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG'
    image_url = 'https://miro.medium.com/max/821/1*Fi6masemXJT3Q8YWekQCDQ.png'

    gfeed = GoogleTrendingSearch(feed_url)
    gfeed.get_feed_data_today()

    try:
        f = open("file.p", "rb")
        posted_array = pickle.load(f)
        f.close()
    except:
        f = open("file.p", 'wb')
        pickle.dump(posted_array, f)
        f.close()

    f.close()
    print(posted_array)

    for item in gfeed.feed_array:
        if item.id not in posted_array:
            # write to file instead of local variable
            posted_array.append(item.id)
            print(posted_array)
            f = open("file.p", "wb")
            pickle.dump(posted_array, f)
            f.close()
            print(item)
            break

# test()
