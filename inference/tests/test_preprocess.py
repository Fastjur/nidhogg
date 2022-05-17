import unittest


from sklearn.feature_extraction.text import TfidfVectorizer

from inference.src.data.preprocess import process_question, preprocess_sentences


class MyTestCase(unittest.TestCase):
    def test_process_question(self):
        teststring = process_question("Is C++ better than C#?")
        self.assertEqual("c++ better c#", teststring)

    def test_preprocess_sentences(self):
        X_train = ["Is javascript the best language?", "Is C++ better than C#?", "Is javascript the best language?", "Is C++ better than C#?", "Is javascript the best language?"]
        vectorizer = TfidfVectorizer(min_df=1, max_df=100, ngram_range=(1,2), token_pattern='(\S+)')
        vectorizer.fit_transform(X_train)
        res = preprocess_sentences(X_train, vectorizer)
        self.assertEqual((5, 17), res.shape)
        self.assertEqual(12, res.nnz)




if __name__ == '__main__':
    unittest.main()
