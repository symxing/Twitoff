import tweepy
import spacy
from .models import DB, Tweet, User
import pandas
import os 

twitter_key = 'uqwtoaKnxgXCwIiwQLXJOiLY8'
twitter_key_secret = 'IPxCBtctFjyyn4RGEQs9TXc7WAjF9dUAN8x4TEDmAknnnODTyQ'
twitter_auth = tweepy.OAuthHandler(twitter_key, twitter_key_secret)
twitter = tweepy.API(twitter_auth)

def add_or_update_user(handle):
    try:
        twitter_user = twitter.get_user(handle)
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, 
            tweet_mode='extended', since_id=db_user.newest_tweet_id
        )

        for tweet in tweets:

            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(e)

    else:
        DB.session.commit()
