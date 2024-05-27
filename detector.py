from joblib import load
from data_functions import *

# Load the model
model = load('model_logistic.joblib')

# Load the vectorizer
vectorizer = load('vectorizer.joblib')

new_article = '''
A secret potion discovered in an ancient Egyptian tomb is said to grant immortality. Researchers who decoded the hieroglyphics on the tomb claim the potion can stop the aging process and heal all diseases, making it the ultimate elixir of life.
'''
new_article = clean_text(new_article)

new_article_vectorized = vectorizer.transform([new_article])

prediction = model.predict(new_article_vectorized)

if prediction[0] == 1:
    print("Fake news")
else:
    print("True news")
