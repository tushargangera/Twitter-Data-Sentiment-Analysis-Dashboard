import os
import numpy as np
from translate import Translator
# from googletrans import Translator
import pandas as pd
import re
from emot.emo_unicode import UNICODE_EMOJI, EMOJI_UNICODE, EMOTICONS_EMO
import string


tweets = [("اهلاً وسهلاً:blush: طلبك قيد التنفيذ حالياً وسيتم إشعارك برسالة نصية حين الرد على طلبك . نشكر تواصلك معنا . تحياتي"),
          ("Iعزيزي العميل نعتذر منك كما طلبك قيد التنفيذ حالياً وسيتم إشعارك برسالة نصية حين الرد على طلبك . نشكر تواصلك معنا . تحياتي"), ("رجى التواصل معنا على الرقم 920000330 خدمة عملاء كويك باي. تحياتي :rose:")]
df = pd.DataFrame(tweets, columns=['arabic'])

class TweetEnglishAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def en_tweets_to_data_frame(tweets):
        # pd.set_option('display.max_colwidth', None)
        # df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df = pd.DataFrame(tweets)

        # df['id'] = np.array([tweet.id for tweet in tweets])
        # df['len'] = np.array([len(tweet.text) for tweet in tweets])
        # df['date'] = np.array([tweet.created_at for tweet in tweets])
        # df['source'] = np.array([tweet.source for tweet in tweets])
        # df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        # df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        def convert_emojis(text):
            for emot in UNICODE_EMOJI:
                text = text.replace(emot, "_".join(
                    UNICODE_EMOJI[emot].replace(",", "").replace(":", "").split()))
            return text
        # Function for converting emoticons into word
        def convert_emoticons(text):
            # text = re.escape(text)
            for emot in EMOTICONS_EMO:
                text = text.replace(emot, "_".join(
                    EMOTICONS_EMO[emot].replace(",", "").split()))
            return text
        def data_cleaning(text):
            # clean-up:
            # remove qutoions
            text = text.strip()
            text = re.sub(r'http\S+', '', text)
            text = re.sub(r'ي+', 'ي', text)
            text = text.replace("آ", "ا")
            text = text.replace("إ", "ا")
            text = text.replace("أ", "ا")
            text = text.replace("ؤ", "و")
            text = text.replace("ئ", "ي")
            text = re.sub(r'[@|#]\S*', '', text)
            text = re.sub(r'"+', '', text)
            # Remove arabic signs
            # text= re.sub(r'([@A-Za-z0-9_ـــــــــــــ]+)|[^\w\s]|#|http\S+', '', text)
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            # Remove repeated letters like "الللللللللللللللله" to "الله"
            text = text[0:2] + ''.join([text[i] for i in range(2, len(text))
                                       if text[i] != text[i-1] or text[i] != text[i-2]])
            text = re.sub(r'D', ':D', text)
            text = re.sub(r'هه+', 'face_with_tears_of_joy', text)
            text = convert_emojis(text)
            text = convert_emoticons(text)
            # Removing punctuations in string
            text = text.translate(str.maketrans('', '', string.punctuation))
            text = re.sub(r'(?:^| )\w(?:$| )', ' ', text)
            text = re.sub(r"$\d+\W+|\b\d+\b|\W+\d+$", "", text)
            text = re.sub(" \d+", " ", text)
            text = re.sub("(\s\d+)", "", text)
            text = re.sub(r'\s+', ' ', text)
            text = re.sub("(\s\d+)", "", text)
            # Returns: hi what is the weather like
            return text
        
        # translator = Translator()
        
        # def translate_text(text):
        #     translation = translator.translate(text, src='ar', dest='en')
        #     return translation.text

        # # translator = Translator()
        # # translator = translator.translate(src='ar', dest='en')
        # df['en_tweets'] = np.array([translate_text(tweet)
        #                            for tweet in df['tweets']])

        translator = Translator(from_lang='ar', to_lang='en')
        df['preprocessing'] = np.array([translator.translate(tweet)
                                   for tweet in df['tweets']])

        df['text'] = df['preprocessing'].apply(lambda x: data_cleaning(x))
        # df['preprocessing'] =df['preprocessing'] .apply(lambda x:arabert_prep.preprocess(x))
                                    
        print(df)
        # path = "C:\\DEV\\python\\Sentiment\\test"
        # isExist = os.path.exists(path)
        # if not isExist:
        #     os.makedirs(path)
        #     print("The new directory is created!")
        #     df.to_csv(path + "\\part6.csv")
        
        return df