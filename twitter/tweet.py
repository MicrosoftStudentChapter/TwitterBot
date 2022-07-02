import datetime
import tweepy
import sqlite3
from dotenv import load_dotenv
from os import getenv

load_dotenv('../.env')

oauth = tweepy.OAuthHandler(getenv('CONSUMER_KEY'), getenv('CONSUMER_SECRET'))
oauth.set_access_token(getenv("ACCESS_TOKEN"), getenv("ACCESS_SECRET"))

api = tweepy.API(oauth)

connection = sqlite3.connect('../twitterBot.db')
cursor = connection.cursor()
news_list = list(cursor.execute('''SELECT * FROM News ORDER BY CASE WHEN SUBREDDIT = 'usersub' THEN 1 ELSE 2 END, IMPORTANCE DESC LIMIT 10'''))
cursor.close()
for index in range(len(news_list)):
    if news_list[index][1] == 'usersub':
        news_list.insert(-1, news_list.pop(index))

last_tweet = None
tweet = ''
for news_item in news_list:
    if news_item[1] == 'usersub' and last_tweet is not None:
        tweet += "[USER SUBMITTED] "
    if last_tweet is None:
        utc = datetime.datetime.utcnow()
        tweet = f'It\'s Tech News Time for the week [{(utc - datetime.timedelta(days=7)).strftime("%m/%d/%Y")}] - [{utc.strftime("%m/%d/%Y")}]:\n'
    last_tweet = api.update_status(status=f'{tweet}{news_item[3]} ({news_item[6]})\nVia:{news_item[4]}',
                                   in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
