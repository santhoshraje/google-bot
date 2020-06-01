import feedparser
from datetime import date
import pickle


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

    def formatted_lite(self):
        data = ""
        data += self.title + ' (' + self.traffic + ' searches today)' + \
            '\n\n' + self.snippet
        return data

    # Deprecated
    # def formatted_lite_us(self):
    #     data = ""
    #     data += self.title + ' (' + self.traffic + ' searches)' + \
    #         '\n\n' + self.snippet
    #     return data

    def __str__(self):
        return 'FeedObject Full: \n\n' + self.formatted() + '\n'

    def __hash__(self):
        return hash(self.title)


class GoogleTrendingSearch:
    def __init__(self, country):
        self.url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=' + country
        self.display_date = str(date.today().strftime("%d %B %Y"))
        self.feed = feedparser.parse(self.url)
        self.feed_array = []

    def published_today(self, published_date):
        today = date.today().strftime("%d %b")
        if today in published_date:
            return True
        return False

    def get_feed_data_today(self):
        for post in self.feed.entries:
            if self.published_today(post['published']):
                self.feed_array.append(FeedObject(post['title'], post['ht_approx_traffic'], post['ht_news_item_title'],
                                                  post['ht_news_item_snippet'], post['ht_news_item_url'], post['ht_picture']))

    def get_feed_data_all(self):
        for post in self.feed.entries:
            self.feed_array.append(FeedObject(post['title'], post['ht_approx_traffic'], post['ht_news_item_title'],
                                              post['ht_news_item_snippet'], post['ht_news_item_url'], post['ht_picture']))

