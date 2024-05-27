from joblib import load
from data_functions import *

# Load the model
model = load('model_bayes.joblib')

# Load the vectorizer
vectorizer = load('vectorizer.joblib')

new_article = '''
In a groundbreaking discovery, a team of scientists has confirmed that the lost city of Atlantis has been found off the coast of Florida. Advanced sonar imaging has revealed the ruins of a vast underwater city, believed to be Atlantis.
'''
new_article = clean_text(new_article)

new_article_vectorized = vectorizer.transform([new_article])

prediction = model.predict(new_article_vectorized)

if prediction[0] == 1:
    print("Fake news")
else:
    print("True news")
