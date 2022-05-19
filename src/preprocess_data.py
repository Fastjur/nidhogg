from ast import literal_eval
import numpy as np
import os
import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from scipy import sparse

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# TODO downloading the stopwords could be handled better
# TODO move vectorizer hyperparameter elsewhere

def process_question(text):
    """
        text: a string
        
        return: modified initial string
    """
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

def train_tfidf_vectorizer(X_train):
    """
        X_train, X_val, X_test — samples        
        return TF-IDF vectorized representation of each sample and vocabulary
    """
    tfidf_vectorizer = TfidfVectorizer(min_df=5, max_df=0.9, ngram_range=(1,2), token_pattern='(\S+)')
    X_train = tfidf_vectorizer.fit_transform(X_train)
    
    return tfidf_vectorizer

def read_data(filename):
    data = pd.read_csv(filename, sep='\t')
    data['tags'] = data['tags'].apply(literal_eval)
    return data

def count_tags_and_words(X_train, y_train):
    # Dictionary of all tags from train corpus with their counts.
    tags_counts = {}
    # Dictionary of all words from train corpus with their counts.
    words_counts = {}

    for sentence in X_train:
        for word in sentence.split():
            if word in words_counts:
                words_counts[word] += 1
            else:
                words_counts[word] = 1

    for tags in y_train:
        for tag in tags:
            if tag in tags_counts:
                tags_counts[tag] += 1
            else:
                tags_counts[tag] = 1
    return (tags_counts, words_counts)

def preprocess_data(raw_data_folder, processed_data_folder, model_folder):
    train = read_data(raw_data_folder + '/train.tsv')
    validation = read_data(raw_data_folder + '/validation.tsv')
    test = pd.read_csv(raw_data_folder + '/test.tsv', sep='\t')

    X_train, y_train = train['title'].values, train['tags'].values
    X_val, y_val = validation['title'].values, validation['tags'].values
    X_test = test['title'].values

    (tags_counts, word_counts) = count_tags_and_words(X_train, y_train)

    vectorizer = train_tfidf_vectorizer(X_train)
    vocab = vectorizer.vocabulary_

    X_train = preprocess_sentences(X_train, vectorizer)
    X_val = preprocess_sentences(X_val, vectorizer)
    X_test = preprocess_sentences(X_test, vectorizer)

    mlb = MultiLabelBinarizer(classes=sorted(tags_counts.keys()))
    y_train = mlb.fit_transform(y_train)
    y_val = mlb.fit_transform(y_val)

    if not os.path.exists(processed_data_folder):
        os.makedirs(processed_data_folder)
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)

    np.savetxt(processed_data_folder + '/tags.txt', sorted(tags_counts.keys()), fmt='%s')
    sparse.save_npz(processed_data_folder + '/X_train.npz', X_train)
    sparse.save_npz(processed_data_folder + '/X_val.npz', X_val)
    sparse.save_npz(processed_data_folder + '/X_test.npz', X_test)

    with open(f"{model_folder}/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    
    with open(f'{processed_data_folder}/y_train.npy', 'wb') as f:
        np.save(f, y_train)
    
    with open(f'{processed_data_folder}/y_val.npy', 'wb') as f:
        np.save(f, y_val)
