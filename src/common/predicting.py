""" Common library for prediction with trained model. """

def predict(preprocessed_sentence, model, tags):
    """ Returns prediction from model. """
    prediction = model.predict(preprocessed_sentence)
    return list(tags[prediction[0] == 1])
