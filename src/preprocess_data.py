from ast import literal_eval
import numpy as np
import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from scipy import sparse

from common.preprocessing import preprocess_sentences

# TODO move vectorizer hyperparameters elsewhere
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

# TODO merge code below with preprocess_data method
if __name__ == "__main__":
    raw_data_folder = "./data"
    processed_data_folder = "./outputs/processed_data"
    model_folder = "./outputs/models"
    preprocess_data(raw_data_folder, processed_data_folder, model_folder)
