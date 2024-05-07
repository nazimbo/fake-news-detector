from joblib import load
from data_functions import *

# Load the model
model = load('model.joblib')

# Load the vectorizer
vectorizer = load('vectorizer.joblib')

new_article = '''

'''
new_article = clean_text(new_article)

new_article_vectorized = vectorizer.transform([new_article])

prediction = model.predict(new_article_vectorized)

if prediction[0] == 1:
    print("Fake news")
else:
    print("True news")
