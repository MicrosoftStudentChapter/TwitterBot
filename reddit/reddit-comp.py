from os import getenv
import praw  # pip install praw
from dotenv import load_dotenv  # pip install python-dotenv
import sqlite3
from get_trends import hot
load_dotenv()

with open('reddit/interest.txt', 'r') as file:
    interesting_boring = file.read().splitlines()  # wanted and unwanted keywords
interesting_keywords = set(interesting_boring[0].lower().split())
trends = set(hot(consumer_key=getenv('CONSUMER_KEY'), consumer_secret=getenv('CONSUMER_SECRET'),
                            access_token=getenv("ACCESS_TOKEN"), access_secret=getenv("ACCESS_SECRET")))
interesting_keywords = interesting_keywords.union(trends)

boring_keywords = set(interesting_boring[1].lower().split())


subreddit_str = "tech+programming+technews+technology"  # subreddits searched seperated with '+'
load_dotenv()
reddit = praw.Reddit(
    client_id=getenv('CLIENT_ID'),
    client_secret=getenv('CLIENT_SECRET'),
    user_agent=getenv("USER_AGENT"),
)

connection = sqlite3.connect('twitterBot.db')
cursor = connection.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS News(ID VARCHAR(10) PRIMARY KEY, SUBREDDIT VARCHAR(50), FLAIR VARCHAR(50), 
    TITLE VARCHAR(500) UNIQUE, URL VARCHAR(255) UNIQUE, RATIO FLOAT, SCORE INT, TOTALCOMMENTS INT, IMPORTANCE INT, SEEN BITINT);''')  # table schema
connection.commit()

subreddit = reddit.subreddit(subreddit_str)
for submission in subreddit.top(limit=25, time_filter="day"):  # top 25 posts of the day across mentioned subreddits
    if (submission.link_flair_text is None) or (
            'business' not in submission.link_flair_text.lower()):  # no business tech news
        interest_factor = 1 + len(set(submission.title.lower().split()).intersection(interesting_keywords)) - (
            len(set(submission.title.lower().split()).intersection(boring_keywords)))

        info = (
            submission.id, submission.subreddit.display_name, submission.link_flair_text, submission.title,
            submission.url, submission.upvote_ratio, submission.score, submission.num_comments,
            int(interest_factor * (submission.upvote_ratio * submission.score + submission.num_comments)), 0)

        cursor.execute(f'''INSERT OR REPLACE INTO News VALUES (?,?,?,?,?,?,?,?,?,?)''', info)  # insert into database
connection.commit()
cursor.close()
