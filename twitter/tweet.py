import datetime
import tweepy  # TODO: Might need to change tokens
import sqlite3
from dotenv import load_dotenv
from os import getenv

load_dotenv('../.env')

client = tweepy.Client(consumer_key=getenv('CONSUMER_KEY'),
                       consumer_secret=getenv('CONSUMER_SECRET'),
                       access_token=getenv("ACCESS_TOKEN"),
                       access_token_secret=getenv("ACCESS_SECRET"))

connection = sqlite3.connect('../twitterBot.db')
cursor = connection.cursor()
news_list = list(cursor.execute(
    '''SELECT * FROM News ORDER BY CASE WHEN SUBREDDIT = 'usersub' THEN 1 ELSE 2 END, IMPORTANCE DESC LIMIT 10'''))
cursor.close()
if len(news_list) < 3:
    exit()
for index in range(len(news_list)):
    if news_list[index][1] == 'usersub':
        news_list.insert(-1, news_list.pop(index))

last_tweet = None
for news_item in news_list:
    if news_item[1] == 'usersub' and last_tweet is not None:
        tweet = "[USER SUBMITTED] "
    elif last_tweet is None:
        utc = datetime.datetime.utcnow()
        tweet = f'It\'s #TechNews Time for the week [{(utc - datetime.timedelta(days=7)).strftime("%m/%d/%Y")}] - [{utc.strftime("%m/%d/%Y")}]:\n '
    else:
        tweet = ''
    last_tweet = client.create_tweet(
        text=f'{tweet}{news_item[3]} ({news_item[8]}) {("#" + news_item[2].replace(" ", "").replace("/", " #")) if news_item[2] is not None else "#news"}\nVia:{news_item[4]}',
        in_reply_to_tweet_id=int(
            last_tweet.data['id']) if last_tweet is not None else None)
    client.like(last_tweet.data['id'])

cursor.execute('''DROP TABLE News''')
connection.commit()

