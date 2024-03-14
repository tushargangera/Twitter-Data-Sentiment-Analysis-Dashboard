import tweepy
from tweepy import API 
from tweepy import Cursor
from tweepy import OAuthHandler

from textblob import TextBlob
from en_tweets import TweetEnglishAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import configparser
import os
from wordcloud import WordCloud

# read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 3
        elif analysis.sentiment.polarity == 0:
            return 2
        else:
            return 1

api = tweepy.API(auth)

# search tweets
search_query = ['QuickPay_SNB', 'snbalahli', 'SNBCares', 'Capital_SNB']
limit=500
since_date = "2023-01-01"

# create DataFrame
columns = ['id', 'created', 'tweetId', 'tweets', 'len', 'source', 'topic', 'tweet_like_count', 'tweet_retweet_count', 'hashtags']
data = []

# Iterate over the search queries
for query in search_query:
    tweets_search = tweepy.Cursor(api.search_tweets, q=query, tweet_mode="extended").items(30)

    for tweet in tweets_search:
        data.append([tweet.id, tweet.created_at, tweet.user.screen_name, tweet.full_text, len(tweet.full_text), tweet.source, query, tweet.favorite_count, tweet.retweet_count, [tag['text'] for tag in tweet.entities['hashtags']]])

df1 = pd.DataFrame(data, columns=columns)

# Delect rows based on inverse of column values
df1 = df1[(df1.tweetId.isin(search_query)==False)]

# df = df.sort_values(by=['date'], ascending=False)

print(df1)

df = TweetEnglishAnalyzer.en_tweets_to_data_frame(df1)

# path = "C:\\Users\\tgangera.I-FLEX\\Downloads\\SNB_POC_BDA\\TwitterAnalysis+BDA\\Result"
# df.to_csv(path + "\\part2.csv")

tweet_analyzer = TweetAnalyzer()

df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['text']])

path = "C:\\Users\\tgangera.I-FLEX\\Downloads\\Twitter_Sentiment_Analysis_Dashboard"
df1.to_csv(path + "\\tweet_sentiment.csv")

print(df.head(10))

# Sentiment Analysis:
df.groupby(['sentiment']).count().plot(kind='pie', y='text', autopct='%1.0f%%', title='Sentiment Analysis on SNB')
plt.show()

# Create a list to store tweet texts
tweet_texts = []

# Join the tweet texts into a single string
text_data = ' '.join(df['text'])

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(text_data)

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

# Save the plot as a PNG file
plt.savefig('All_Topics.png', dpi=300, bbox_inches='tight')