import os
import unittest


from sklearn.feature_extraction.text import TfidfVectorizer

from src.common.preprocessing import get_stopwords, process_question, preprocess_sentences


class MyTestCase(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        if not os.path.exists("outputs/nltk_corpora"):
            os.makedirs("outputs/nltk_corpora")
        self.stopwords = get_stopwords("outputs/nltk_corpora/")

    def test_process_question(self):
        teststring = process_question("Is C++ better than C#?", self.stopwords)
        self.assertEqual("c++ better c#", teststring)

    def test_preprocess_sentences(self):
        X_train = [
            "Is javascript the best language?",
            "Is C++ better than C#?",
            "Is javascript the best language?",
            "Is C++ better than C#?",
            "Is javascript the best language?"]
        vectorizer = TfidfVectorizer(
            min_df=1, max_df=100, ngram_range=(
                1, 2), token_pattern='(\\S+)')
        vectorizer.fit_transform(X_train)
        res = preprocess_sentences(X_train, vectorizer, self.stopwords)
        self.assertEqual((5, 17), res.shape)
        self.assertEqual(12, res.nnz)


if __name__ == '__main__':
    unittest.main()
