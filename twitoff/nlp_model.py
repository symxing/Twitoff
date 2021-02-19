import spacy

class NLP():
    def __init__(self):
        #Load English pipeline
        self.nlp = spacy.load('en_core_web_sm') #small models
        #  https://spacy.io/models

    def vectorize_tweet(self, tweet_text):
        doc = self.nlp(tweet_text)
        return doc.vector
