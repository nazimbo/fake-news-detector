from joblib import load
from data_functions import *

# Load the model
model = load('model.joblib')

# Load the vectorizer
vectorizer = load('vectorizer.joblib')

new_article = "The Israeli military seized control of the Rafah border crossing between the Gaza Strip and Egypt on Tuesday and its tanks pushed into the southern Gazan town of Rafah after a night of air strikes on the Palestinian enclave."
new_article = clean_text(new_article)

new_article_vectorized = vectorizer.transform([new_article])

prediction = model.predict(new_article_vectorized)

if prediction[0] == 1:
    print("Fake news")
else:
    print("True news")
