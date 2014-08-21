#import requests
import json
import urllib2

# USAToday article API: hve6vyzvx78gjrb4kxy9mjdg
api_key = "hve6vyzvx78gjrb4kxy9mjdg"
url = "http://api.usatoday.com/open/articles" \
      "/topnews/tech?count=10&days=0&page=0&encoding=json&api_key=" + api_key
data = json.load(urllib2.urlopen(url))
stories =  data['stories']
# for key, value in data.iteritems():
#     print key, value
for story in stories:
    #print story['link']
    print story['pubDate']
    print story['description']
    #print story['title'], story['link']
