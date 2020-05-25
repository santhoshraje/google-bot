  #!/usr/bin/env python
# -*- coding: utf-8 -*-
from trending_searches_rss import GoogleTrendingSearch
import schedule
import time
import pickle
from threading import Thread
import os
from bot import Bot

subscribed = False
chat_id = 0
my_context = 0
my_update = 0

# Command handler
def start(update, context):
    global chat_id 
    chat_id = update.effective_chat.id
    global my_context 
    my_context = context
    global my_update
    my_update = update
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def rss(update, context):
    #context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(rssdata())

def subscribe(update, context):
    global subscribed
    subscribed = True
    context.bot.send_message(chat_id=update.effective_chat.id, text="Subscribed to Google Tending Searches feed")

def unsubscribe(update, context):
    global subscribed
    subscribed = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="Subscribed from Google Tending Searches feed")

def send_feed(item = 'bye world', update = 0, context = 0):
    global chat_id
    global my_context
    url = 'https://miro.medium.com/max/821/1*Fi6masemXJT3Q8YWekQCDQ.png'
    my_context.bot.send_photo(chat_id = chat_id,
     photo=url,
     caption = item)

def feedchecker():
    # url to use 
    url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG'
    # google rss feed
    gfeed = GoogleTrendingSearch(url)
    # get feed every 30 mins and dump into file
    schedule.every(0.5).minutes.do(gfeed.get_feed_data_today)
    # main loop
    while True:
        # run scheduled tasks
        schedule.run_pending()
        # if file is empty (poster is done with it)
        if not os.path.getsize("feed.p") > 0:
            # check if feed exists
            if gfeed.feed_array:
                print('array not empty')
                # open the file
                f = open('feed.p', 'wb')
                # overwrite existing content
                pickle.dump(gfeed.feed_array, f)
                #close the file
                f.close()    
                gfeed.feed_array.clear()
            else:
                print('array empty')
        time.sleep(1)

def poster():
    open("posted.p", 'w').close()
    finished = False
    while True:
        finished = True
        print('running')
        f = open("feed.p", "rb")
        fdata = pickle.load(f)
        f.close()
        # if poster is empty
        if not os.path.getsize("posted.p") > 0:
            print('posted file is empty')
            b = open("posted.p", "wb")
            bdata = [0]
            pickle.dump(bdata, b)
            b.close()

        a = open("posted.p", "rb")
        posted_array = pickle.load(a)
        a.close()

        for item in fdata:
            if item.id not in posted_array:
                finished = False
                # send message

                # update posted file
                posted_array.append(item.id)
                z = open("posted.p", "wb")
                pickle.dump(posted_array, z)
                z.close()
                break

        if finished:
            print('finished posting')

        time.sleep(60)

        

def main():

    bot = Bot()
    bot.start_bot()

    

    # # telegram api
    # updater = Updater(load('BOT_TOKEN'), use_context=True)

    # # Get the dispatcher to register handlers
    # dp = updater.dispatcher

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("subscribe", subscribe))
    # dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    # dp.add_handler(CommandHandler("feed", send_feed))

    # Start the Bot
    # updater.start_polling()

    # updater.idle()

if __name__ == '__main__':
    main()