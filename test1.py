import pandas as pd
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
from googletrans import Translator
from wordcloud import WordCloud

df = pd.read_csv('C:\\Users\\tgangera.I-FLEX\\Downloads\\Twitter_Sentiment_Analysis_Dashboard\\tweet_sentiment.csv', encoding='latin-1')
print(df)

df['text']=df['text'].to_string()

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