from telegram.ext import Updater, CommandHandler
from config_loader import get_config_value as load
from trending_searches_rss import GoogleTrendingSearch

class Bot:
    def __init__(self):
        self.token = load('BOT_TOKEN')
        # telegram api
        self.updater = Updater(self.token, use_context=True)
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher   
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("feed", self.google_trending_sg))
        self.dp.add_handler(CommandHandler("channel", self.google_trending_us))
        self.posted_array = [0]
        self.channel_id = ''
        self.image_url = 'https://miro.medium.com/max/821/1*Fi6masemXJT3Q8YWekQCDQ.png'


    def start_bot(self):
        print('bot active')
        self.updater.start_polling()
    
    def start(self, update, context):
        context.bot.send_message(chat_id= update.effective_chat.id, text="I'm a bot, please talk to me!") 
    
    def google_trending_sg(self, update, context):
        feed_url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG'
        # get feed
        gfeed = GoogleTrendingSearch(feed_url)
        gfeed.get_feed_data_today()
        for item in gfeed.feed_array:
            if item.id not in self.posted_array:
                self.posted_array.append(item.id)
                context.bot.send_photo(chat_id = update.effective_chat.id, photo = self.image_url, caption = item.formatted_beta())
                break

    
    def google_trending_us(self, update, context):
        feed_url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=US'
        # get feed
        gfeed = GoogleTrendingSearch(feed_url)
        gfeed.get_feed_data_all()
        for item in gfeed.feed_array:
            if item.id not in self.posted_array:
                self.posted_array.append(item.id)
                context.bot.send_photo(chat_id = self.channel_id, photo = self.image_url, caption = item.formatted_beta_us(), disable_notification = True)
                break



        
    

    
