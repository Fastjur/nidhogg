from ast import literal_eval
import json
import numpy as np
import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score, f1_score, average_precision_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
import sys

from common.preprocessing import get_stopwords, preprocess_sentences


def train_tfidf_vectorizer(X_train):
    """
        X_train, X_val, X_test — samples
        return TF-IDF vectorized representation of each sample and vocabulary
    """
    tfidf_vectorizer = TfidfVectorizer(
        min_df=5, max_df=0.9, ngram_range=(
            1, 2), token_pattern='(\\S+)')  # TODO hyperparameters
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


def preprocess_data(raw_data_folder, nltk_corpora_folder):
    train = read_data(raw_data_folder + '/train.tsv')
    validation = read_data(raw_data_folder + '/validation.tsv')
    test = pd.read_csv(raw_data_folder + '/test.tsv', sep='\t')

    X_train, y_train = train['title'].values, train['tags'].values
    X_val, y_val = validation['title'].values, validation['tags'].values
    X_test = test['title'].values

    (tags_counts, word_counts) = count_tags_and_words(X_train, y_train)

    vectorizer = train_tfidf_vectorizer(X_train)
    vocab = vectorizer.vocabulary_

    stopwords = get_stopwords(nltk_corpora_folder)
    X_train = preprocess_sentences(X_train, vectorizer, stopwords)
    X_val = preprocess_sentences(X_val, vectorizer, stopwords)
    X_test = preprocess_sentences(X_test, vectorizer, stopwords)

    mlb = MultiLabelBinarizer(classes=sorted(tags_counts.keys()))
    y_train = mlb.fit_transform(y_train)
    y_val = mlb.fit_transform(y_val)

    tags = sorted(tags_counts.keys())

    return X_train, y_train, X_val, y_val, X_test, vectorizer, tags


def train_classifier(X_train, y_train, penalty='l1', C=1):
    """
      X_train, y_train — training data

      return: trained classifier
    """
    # Create and fit LogisticRegression wraped into OneVsRestClassifier.

    clf = LogisticRegression(
        penalty=penalty,
        C=C,
        dual=False,
        solver='liblinear')  # TODO hyperparameters
    clf = OneVsRestClassifier(clf)
    clf.fit(X_train, y_train)

    return clf


def report_evaluation_scores(y_val, predicted):
    accuracy = accuracy_score(y_val, predicted)
    f1 = f1_score(y_val, predicted, average='weighted')
    avg_precision = average_precision_score(y_val, predicted, average='macro')
    with open(f"{metrics_folder}/model_metrics.json", "w") as f:
        json.dump({"accuracy": accuracy, "f1": f1,
                  "avg_precision": avg_precision}, f)
    print(
        f"Accuracy: {accuracy} \t F1 score: {f1} \t Average precision: {avg_precision}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python train_model.py [data_folder] [nltk_corpora_folder] [model_folder] [metrics_folder]")
        exit()
    [_, data_folder, nltk_corpora_folder, model_folder, metrics_folder] = sys.argv
    for folder in [model_folder, nltk_corpora_folder, metrics_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    print("Preprocessing data and training vectorizer... ")
    X_train, y_train, X_val, y_val, X_test, vectorizer, tags = preprocess_data(
        data_folder, nltk_corpora_folder)
    print("Done.")

    # Train the model
    print("Training classification model... ", end="", flush=True)
    clf = train_classifier(
        X_train,
        y_train,
        penalty='l2',
        C=10)  # TODO hyperparameters
    print("Done.")

    print("Evaluating model...")
    y_val_predicted = clf.predict(X_val)
    report_evaluation_scores(y_val, y_val_predicted)
    print("Done.")

    print("Saving trained model... ", end="", flush=True)
    with open(f"{model_folder}/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(f"{model_folder}/tfidf_model.pkl", "wb") as f:
        pickle.dump(clf, f)
    np.savetxt(f"{model_folder}/tags.txt", tags, fmt='%s')
    print("Done.")
