import feedparser
from datetime import date

def getFeedData():
    data = ""
    i = 1
    url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG'
    feed = feedparser.parse(url)
    for post in feed.entries:  
         data += str(str(i) + '. ' + 
         post['title'] + ' (' +  
         post['ht_approx_traffic'] + 
         ' searches) \n')
         i+=1
    return data    

def testFeed():
    today = date.today().strftime("%d %B")
    feed = feedparser.parse('https://trends.google.com/trends/trendingsearches/daily/rss?geo=SG')

    for post in feed.entries: 
        if today in str(post['published']):
            title = str(post['title'])
            traffic = str(post['ht_approx_traffic'])
            expanded_title = str(post['ht_news_item_title'])
            snippet = str(post['ht_news_item_snippet'])
            url = str(post['ht_news_item_url'])
            image_url = post['ht_picture']
            # remove unwanted characters
            for r in (("&#39;", "'"), ("&nbsp;", "")):
                title = title.replace(*r)
                traffic = traffic.replace(*r)
                expanded_title = expanded_title.replace(*r)
                snippet = snippet.replace(*r)
                url = url.replace(*r)
            print(title)
            print(traffic)
            print(expanded_title)
            print(snippet)
            print(url)
            print(image_url)
            print('\n')
            
        # print(post.keys())

testFeed()