import feedparser
from datetime import date
import pickle


class GoogleFeed:
    def __init__(self):
        print('Google Feed')

    def get_item(self):
        posted_array = [0]
        # get feed
        tmp = GoogleTrendingSearch('SG').get_feed_data_today()
        # check for empty feed
        if not tmp:
            print('RSS feed is empty')
            return
        # file io
        try:
            f = open("trending.pickle", "rb")
            posted_array = pickle.load(f)
            f.close()
        except:
            f = open("trending.pickle", 'wb')
            pickle.dump(posted_array, f)
            f.close()
        # close the file
        f.close()
        # loop thru items in the array
        for item in tmp:
            # if the item has not already been posted
            if hash(item) not in posted_array:
                # write to file
                posted_array.append(hash(item))
                f = open("trending.pickle", "wb")
                pickle.dump(posted_array, f)
                f.close()
                return item


class FeedObject:
    def __init__(self, title, traffic, expanded_title, snippet, url, image_url):
        self.title = self.sanitize_data(title)
        self.traffic = self.sanitize_data(traffic)
        self.expanded_title = self.sanitize_data(expanded_title)
        self.snippet = self.sanitize_data(snippet)
        self.url = url
        self.image_url = image_url

    def sanitize_data(self, data):
        for r in (("&#39;", "'"), ("&nbsp;", ""), ("&quot;", "'")):
            data = data.replace(*r)
        return data

    def formatted(self):
        data = ""
        data += '<b>' + self.title + '</b> (' + self.traffic + ' searches today)' + \
            '\n\n' + self.snippet + '\n\n' + '<a href="' + \
                self.url + '">' + 'Find out more </a>'
        return data

    def __str__(self):
        return 'FeedObject Full: \n\n' + self.formatted() + '\n'

    def __hash__(self):
        return hash(self.title)


class GoogleTrendingSearch:
    def __init__(self, country):
        self.url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=' + country
        self.feed = feedparser.parse(self.url)
        # self.feed_array = []

    # check if the item from the rss feed was published today
    def published_today(self, published_date):
        today = date.today().strftime("%d %b")
        if today in published_date:
            return True
        return False

    # get all the items from the feed that were posted today
    def get_feed_data_today(self):
        tmp = []
        for post in self.feed.entries:
            if self.published_today(post['published']):
                tmp.append(FeedObject(post['title'], post['ht_approx_traffic'], post['ht_news_item_title'],
                                      post['ht_news_item_snippet'], post['ht_news_item_url'], post['ht_picture']))
        return tmp

    # get all the items from the feed
    def get_feed_data_all(self):
        tmp = []
        for post in self.feed.entries:
            tmp.append(FeedObject(post['title'], post['ht_approx_traffic'], post['ht_news_item_title'],
                                  post['ht_news_item_snippet'], post['ht_news_item_url'], post['ht_picture']))
        return tmp

    # get all possible keys from the feed
    def get_all_keys(self):
        for post in self.feed.entries:
            print(post.keys())
            break
