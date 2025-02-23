from flask import Flask, request, jsonify
from joblib import load
from data_functions import clean_text
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Load the model and the vectorizer
vectorizer = load('models/vectorizer.joblib')


@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json(force=True)

    article = data.get('article', '')
    model_name = data.get('model', 'naive_bayes')
    print(model_name)

    model = load(f'models/model_{model_name}.joblib')

    # Clean and vectorize the article
    cleaned_article = clean_text(article)
    vectorized_article = vectorizer.transform([cleaned_article])

    # Make a prediction
    prediction = model.predict(vectorized_article)

    # Prediction probabilities
    if hasattr(model, 'predict_proba'):
        prediction_proba = model.predict_proba(vectorized_article)
        probabilities = {
            "true": prediction_proba[0][0],
            "fake": prediction_proba[0][1]
        }
    else:
        probabilities = None

    # Return the result as JSON
    result = 'Fake news' if prediction[0] == 1 else 'True news'
    return jsonify({
        'prediction': result,
        'model': model_name.replace("_", " ").title(),
        'probabilities': probabilities
    })


if __name__ == '__main__':
    app.run(debug=True)
