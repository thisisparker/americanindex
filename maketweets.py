import csv
import json
import os
import random

from badwords import badwords

fullpath = os.path.dirname(os.path.realpath(__file__))

def main():
    with open(os.path.join(fullpath, 'index_of_american_design.json')) as f:
        index = json.load(f)

    tweets = []

    for i in index:
        tweet = {}
        if (not any(w in i['title'].lower() for w in badwords) 
                and i.get('download')):
            text = i.get('title').lower()
            text += ' (' + i['displaydate'] + '),' if i.get('displaydate') else ''
            text += ' ' + i['medium'] + ',' if i.get('medium') else ''
            text += ' ' + i['attribution'].lower() if i.get('attribution') else ''
            tweet['text'] = text
            tweet['image_url'] = i['download']
            tweets.append(tweet)    
 
    random.shuffle(tweets)

    return tweets

if __name__ == '__main__':
    main()
