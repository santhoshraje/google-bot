import feedparser

def getFeedData():
    data = ""
    i = 1
    url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG'
    feed = feedparser.parse(url)
    for post in feed.entries:  
         data += str(str(i) + '. ' + post['title'] + ' (' +  post['ht_approx_traffic'] + ' searches) \n')
         i+=1
    return data    

def testFeed():
    feed = feedparser.parse('https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG')
    for post in feed.entries: 
        print(post['title'])
        print(post['ht_approx_traffic'])
        print(post['ht_news_item_title'])

testFeed()