import tweepy

def hot(consumer_key: str, consumer_secret: str, access_token: str, access_secret: str, woeid: int = 2488042):
    oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(oauth)
    oauth.set_access_token(access_token, access_secret)
    trends = api.get_place_trends(woeid)
    trends = [x['name'] for x in trends[0]['trends']]
    trends_processed = [x.replace("_", " ").replace("#", "").lower() for x in trends]
    return trends_processed

