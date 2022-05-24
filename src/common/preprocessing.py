import re

# TODO downloading the stopwords could be handled better
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def process_question(text):
    """ Takes question text to be processed for consumption by model. """
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))
    text = text.lower() # lowercase text
    text = re.sub(REPLACE_BY_SPACE_RE, " ", text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = re.sub(BAD_SYMBOLS_RE, "", text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = " ".join([word for word in text.split() if not word in STOPWORDS]) # delete stopwords from text
    return text

def preprocess_sentences(X_vals, vectorizer):
    X_vals = [process_question(x) for x in X_vals]
    X_vals = vectorizer.transform(X_vals)
    return X_vals

def preprocess_sentence(sentence, vectorizer):
    sentence = process_question(sentence)
    sentence = vectorizer.transform([sentence])
    return sentence
