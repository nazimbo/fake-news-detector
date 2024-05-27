from joblib import load
from data_functions import *

# Load the model
model = load('model_logistic.joblib')

# Load the vectorizer
vectorizer = load('vectorizer.joblib')

new_article = '''
The U.S. Centers for Disease Control and Prevention (CDC) said on Monday it had seen a higher-than-expected number of cases of heart inflammation among young people, who received an mRNA COVID-19 vaccine, and had requested that healthcare providers be on alert for cases of myocarditis.
'''
new_article = clean_text(new_article)

new_article_vectorized = vectorizer.transform([new_article])

prediction = model.predict(new_article_vectorized)

if prediction[0] == 1:
    print("Fake news")
else:
    print("True news")
