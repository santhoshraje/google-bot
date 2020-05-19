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
        data += self.title + ' (' + self.traffic + ' searches today)' + \
            '\n\n' + self.snippet + '\n\n' + 'Find out more: ' + self.url
        return data

    def __str__(self):
         return 'FeedObject: \n\n' + self.formatted() + '\n'


class GoogleTrendingSearch:
    def __init__(self, url):
        self.url = url
        self.display_date = str(date.today().strftime("%d %B %Y"))
        self.feed = feedparser.parse(url)
        self.feed_array = []


    def published_today(self, published_date):
        today = date.today().strftime("%d %B")
        if today in published_date:
            return True
        return False

    def get_feed_data_today(self):
        for post in self.feed.entries:
            if self.published_today(post['published']):
                self.feed_array.append(FeedObject(post['title'], post['ht_approx_traffic'], post['ht_news_item_title'],
                                       post['ht_news_item_snippet'], post['ht_news_item_url'], post['ht_picture']))       

def main():
    g1 = GoogleTrendingSearch('https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG')
    for o in g1.get_feed_data_today():
        print(o)

# main()




# def testFeed():
#     today = date.today().strftime("%d %B")
#     display_date = str(date.today().strftime("%d %B %Y"))
#     feed = feedparser.parse(
#         'https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG')
#     data = ""

#     for post in feed.entries:
#         # if the article was posted today
#         if today in str(post['published']):
#             title = str(post['title'])
#             traffic = str(post['ht_approx_traffic'])
#             expanded_title = str(post['ht_news_item_title'])
#             snippet = str(post['ht_news_item_snippet'])
#             url = str(post['ht_news_item_url'])
#             image_url = post['ht_picture']

#             # remove unwanted characters
#             for r in (("&#39;", "'"), ("&nbsp;", "")):
#                 title = title.replace(*r)
#                 traffic = traffic.replace(*r)
#                 expanded_title = expanded_title.replace(*r)
#                 snippet = snippet.replace(*r)
#                 url = url.replace(*r)

#             data += title + ' (' + traffic + ' searches today)' + \
#                 '\n\n' + snippet + '\n\n' + 'Find out more: ' + url

#             print(display_date)
#             print(title)
#             print(traffic)
#             print(expanded_title)
#             print(snippet)
#             print(url)
#             print(image_url)
#             print('\n')
#             print(data)
#             print(post.keys())
#             return data


