import numpy as np
import pickle
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score
from scipy import sparse

from preprocess_data import preprocess_sentence

# TODO add evaluation of model to train file

def print_evaluation_scores(y_val, predicted):
    print('Accuracy score: ', accuracy_score(y_val, predicted))
    print('F1 score: ', f1_score(y_val, predicted, average='weighted'))
    print('Average precision score: ', average_precision_score(y_val, predicted, average='macro'))

def evaluate():
    clf = pickle.load(open(f"{model_folder}/tfidf_model.pkl", "rb"))
    X_val_tfidf = sparse.load_npz(f'{processed_data_folder}/X_val.npz')
    y_val = np.array([])
    with open(f"{processed_data_folder}/y_val.npy", "rb") as f:
        y_val = np.load(f)

    y_val_predicted_labels_tfidf = clf.predict(X_val_tfidf)
    y_val_predicted_scores_tfidf = clf.decision_function(X_val_tfidf)
    print_evaluation_scores(y_val, y_val_predicted_labels_tfidf)
