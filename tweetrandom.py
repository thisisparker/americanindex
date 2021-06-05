#!/usr/bin/env python3

import csv
import os

import requests
import yaml

from io import BytesIO
from twython import Twython
from PIL import Image

import maketweets

fullpath = os.path.dirname(os.path.realpath(__file__))
tweets_file = os.path.join(fullpath, 'shuffled_tweets.csv')

with open(os.path.join(fullpath, "config.yaml")) as f:
    config = yaml.safe_load(f)

open(tweets_file, 'a').close()

with open(tweets_file) as f:
    reader = csv.DictReader(f)
    tweets = list(reader)
    if not tweets:
        tweets = maketweets.main()

tweet = tweets.pop(0)

with open(tweets_file, "w") as f:
    writer = csv.DictWriter(f, ['text', 'image_url'])
    writer.writeheader()
    writer.writerows(tweets)

twitter_app_key = config['twitter_app_key']
twitter_app_secret = config['twitter_app_secret']
twitter_oauth_token = config['twitter_oauth_token']
twitter_oauth_token_secret = config['twitter_oauth_token_secret']

twitter = Twython(twitter_app_key, twitter_app_secret, twitter_oauth_token, twitter_oauth_token_secret)

res = requests.get(tweet['image_url'])

img = Image.open(BytesIO(res.content))
img_io = BytesIO()
img.save(img_io, format='jpeg')

img_io.seek(0)

# Twitter upload, tweet

response = twitter.upload_media(media=img_io)
twitter.update_status(status=tweet['text'], media_ids=[response['media_id']])
