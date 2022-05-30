import nltk
from nltk.downloader import Downloader

import re

def get_stopwords(download_dir):
    nltk.data.path = [download_dir]
    downloader = Downloader(download_dir=download_dir)
    if not downloader.is_installed("stopwords"):
        print("Downloading nltk stopwords corpus... ", end="", flush=True)
        nltk.download("stopwords", download_dir)
        print("Done.")
    from nltk.corpus import stopwords
    return stopwords

def process_question(text, stopwords):
    """ Takes question text to be processed for consumption by model. """
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))
    text = text.lower() # lowercase text
    text = re.sub(REPLACE_BY_SPACE_RE, " ", text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = re.sub(BAD_SYMBOLS_RE, "", text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = " ".join([word for word in text.split() if not word in STOPWORDS]) # delete stopwords from text
    return text

def preprocess_sentences(X_vals, vectorizer, stopwords):
    X_vals = [process_question(x, stopwords) for x in X_vals]
    X_vals = vectorizer.transform(X_vals)
    return X_vals

def preprocess_sentence(sentence, vectorizer, stopwords):
    sentence = process_question(sentence, stopwords)
    sentence = vectorizer.transform([sentence])
    return sentence