from flask import Flask, request, jsonify
from joblib import load
from data_functions import clean_text
from flask_cors import CORS
import os
import logging
import os
from dotenv import load_dotenv
import nltk

# Download required NLTK data
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)
    logging.info("NLTK resources downloaded successfully")
except Exception as e:
    logging.error(f"Error downloading NLTK resources: {str(e)}")

load_dotenv()  # Load environment variables

# Initialize the Flask application
app = Flask(__name__)

# Restrict CORS to frontend URL only
CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://fake-news-detector-eta.vercel.app",
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define allowed models to prevent path traversal
ALLOWED_MODELS = ["naive_bayes", "logistic_regression", "random_forest"]

# Global variables for models and vectorizer
models = {}
vectorizer = None


def load_models():
    """Load all models and vectorizer at startup"""
    global models, vectorizer

    try:
        # Check if models directory exists
        models_dir = "models"
        if not os.path.exists(models_dir):
            logger.error(f"Models directory '{models_dir}' does not exist")
            logger.info(f"Current working directory: {os.getcwd()}")
            logger.info(f"Directory contents: {os.listdir('.')}")
            raise FileNotFoundError(f"Models directory not found")

        # Load vectorizer
        vectorizer_path = "models/vectorizer.joblib"
        if not os.path.exists(vectorizer_path):
            logger.error(f"Vectorizer not found at {vectorizer_path}")
            logger.info(f"Models directory contents: {os.listdir(models_dir)}")
            raise FileNotFoundError(f"Vectorizer not found at {vectorizer_path}")
        vectorizer = load(vectorizer_path)
        logger.info("Vectorizer loaded successfully")

        # Load models
        for model_name in ALLOWED_MODELS:
            model_path = f"models/model_{model_name}.joblib"
            if os.path.exists(model_path):
                models[model_name] = load(model_path)
                logger.info(f"Model {model_name} loaded successfully")
            else:
                logger.warning(f"Model {model_name} not found at {model_path}")

        if not models:
            logger.error("No models were loaded successfully")
            logger.info(f"Models directory contents: {os.listdir(models_dir)}")
            raise Exception("No models were loaded successfully")

        logger.info(f"Successfully loaded {len(models)} models: {list(models.keys())}")

    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        logger.error(f"Current working directory: {os.getcwd()}")
        if os.path.exists("models"):
            logger.error(f"Models directory contents: {os.listdir('models')}")
        raise


# Load models at startup
load_models()


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        article = data.get("article", "").strip()
        model_name = data.get("model", "naive_bayes")

        # Validate inputs
        if not article:
            return jsonify({"error": "Article text is required"}), 400

        # Validate model name to prevent path traversal
        if model_name not in ALLOWED_MODELS:
            return (
                jsonify(
                    {
                        "error": f'Invalid model. Allowed models: {", ".join(ALLOWED_MODELS)}'
                    }
                ),
                400,
            )

        # Check if requested model is loaded
        if model_name not in models:
            return jsonify({"error": f"Model {model_name} is not available"}), 404

        # Limit article length to prevent memory issues
        if len(article) > 10000:  # 10KB limit
            return (
                jsonify({"error": "Article text is too long (max 10,000 characters)"}),
                400,
            )

        model = models[model_name]

        # Clean and vectorize the article
        cleaned_article = clean_text(article)
        if not cleaned_article:
            return jsonify({"error": "Article text could not be processed"}), 400

        vectorized_article = vectorizer.transform([cleaned_article])

        # Make a prediction
        prediction = model.predict(vectorized_article)

        # Prediction probabilities
        probabilities = None
        if hasattr(model, "predict_proba"):
            prediction_proba = model.predict_proba(vectorized_article)
            probabilities = {
                "true": float(prediction_proba[0][0]),
                "fake": float(prediction_proba[0][1]),
            }

        # Return the result as JSON
        result = "Fake news" if prediction[0] == 1 else "True news"

        logger.info(f"Prediction made using {model_name}: {result}")

        return jsonify(
            {
                "prediction": result,
                "model": model_name.replace("_", " ").title(),
                "probabilities": probabilities,
            }
        )

    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": "Internal server error occurred"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "models_loaded": list(models.keys()),
            "vectorizer_loaded": vectorizer is not None,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
