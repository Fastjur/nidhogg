from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from scipy import sparse

import pickle
import numpy as np

# TODO configure hyperparameters elsewhere

def train_classifier(X_train, y_train, penalty='l1', C=1):
    """
      X_train, y_train — training data
      
      return: trained classifier
    """
    # Create and fit LogisticRegression wraped into OneVsRestClassifier.
    
    clf = LogisticRegression(penalty=penalty, C=C, dual=False, solver='liblinear')
    clf = OneVsRestClassifier(clf)
    clf.fit(X_train, y_train)
    
    return clf  

def start_training(processed_data_folder, model_folder):
    X_train_tfidf = sparse.load_npz(f"{processed_data_folder}/X_train.npz")
    with open(f"./{processed_data_folder}/y_train.npy", "rb") as f:
        y_train = np.load(f)

    clf = train_classifier(X_train_tfidf, y_train, penalty='l2', C=10)
    with open(f"{model_folder}/tfidf_model.pkl", "wb") as f:
        pickle.dump(clf, f)
