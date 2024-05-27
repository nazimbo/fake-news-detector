from joblib import load
from data_functions import *

# Load the model
model = load('model_logistic.joblib')

# Load the vectorizer
vectorizer = load('vectorizer.joblib')

new_article = '''
The United Nations has issued a call for urgent humanitarian aid to Afghanistan as the country grapples with a worsening crisis. The withdrawal of international forces and the Taliban's takeover have led to widespread displacement, food shortages, and economic collapse. The UN warns that millions of Afghans are at risk of famine and disease without immediate assistance. International donors are urged to provide emergency funding to address the growing humanitarian needs in Afghanistan.
'''
new_article = clean_text(new_article)

new_article_vectorized = vectorizer.transform([new_article])

prediction = model.predict(new_article_vectorized)

if prediction[0] == 1:
    print("Fake news")
else:
    print("True news")
