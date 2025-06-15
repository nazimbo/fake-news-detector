# Fake News Detector

This project is a fake news detector that uses a machine learning model to classify news articles as fake or real. The model is trained on a dataset of news articles that are labeled as fake or real.

## Project Structure

```
fake-news-detector/
├── backend/                    # Python Flask API and ML models
│   ├── app.py                 # Main Flask application
│   ├── detector.py            # Prediction logic
│   ├── data_functions.py      # Data processing utilities
│   ├── data_preparation.py    # Data preprocessing pipeline
│   ├── comparison_functions.py # Model comparison utilities
│   ├── trainer_main.py        # Model training script
│   ├── trainer_hyper.py       # Hyperparameter tuning
│   ├── install_nltk.py        # NLTK data installation script
│   ├── dataset/               # Training data
│   │   ├── cleaned_dataset.csv # Processed dataset
│   │   ├── fake.csv           # Fake news articles
│   │   └── true.csv           # Real news articles
│   ├── models/                # Standard trained ML models
│   │   ├── model_logistic_regression.joblib
│   │   ├── model_naive_bayes.joblib
│   │   ├── model_random_forest.joblib
│   │   └── vectorizer.joblib
│   ├── models_hyperparams/    # Hyperparameter-tuned models
│   │   ├── best_model_logistic_regression.joblib
│   │   ├── best_model_naive_bayes.joblib
│   │   └── vectorizer.joblib
│   ├── graphics/              # Performance visualizations
│   │   ├── classification_report.png
│   │   ├── confusion_matrix.png
│   │   └── roc_curve.png
│   ├── test_articles.json     # Test data for validation
│   ├── notes.txt              # Development notes
│   ├── requirements.txt       # Python dependencies
│   ├── runtime.txt            # Python version for deployment
│   ├── render.yaml            # Render deployment config
│   └── render_build.sh        # Build script for deployment
├── frontend/                   # Vue.js web application
│   ├── src/                   # Source code
│   │   ├── App.vue            # Main Vue component
│   │   ├── main.js            # Application entry point
│   │   ├── style.css          # Global styles
│   │   └── assets/            # Static assets
│   ├── public/                # Public static files
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS config
│   ├── postcss.config.js      # PostCSS configuration
│   └── index.html             # HTML template
└── README.md                  # This file
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher (tested with 3.13.4)
- Node.js 16 or higher (tested with 24.2.0)
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install required NLTK data:
   ```bash
   python install_nltk.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Start the Backend API

1. Navigate to the backend directory and activate your virtual environment:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

   The backend API will be available at `http://127.0.0.1:5000`

### Start the Frontend

1. In a new terminal, navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

### Using the Application

1. Open your web browser and go to `http://localhost:5173`
2. Select a machine learning model (Naive Bayes, Logistic Regression, or Random Forest)
3. Enter the news text you want to analyze
4. Click "Check News" to get the prediction
5. View the result showing whether the news is likely fake or real, along with confidence probability

## Model Training (Optional)

If you want to retrain the models:

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the training script:
   ```bash
   python trainer_main.py
   ```

3. For hyperparameter tuning:
   ```bash
   python trainer_hyper.py
   ```

## API Endpoints

- `POST /predict` - Predict if news is fake or real
  - Request body: `{"article": "news text", "model": "naive_bayes|logistic_regression|random_forest"}`
  - Response: `{"prediction": "Fake news|Real news", "model": "model_name", "probabilities": {"fake": 0.xx, "true": 0.xx}}`

## Dataset

The dataset used to train the model is from Kaggle (https://www.kaggle.com/code/therealsampat/fake-news-detection/input). The dataset contains two CSV files, one with fake news articles and one with real news articles.

## Step 1: Data Preparing

The first step is to prepare the data for training the model. This involves loading the data, removing useless columns, adding a label to each article (fake or real), and combining the two datasets into one shuffled dataset. The function `prepare_data` in `data_functions.py` does this.

## Step 2: Data Cleaning

The next step is to clean the data. This involves lowercasing the text, replacing all non alphabetical characters with spaces, removing stopwords, and lemmatizing the text. The function `clean_data` in `data_functions.py` does this.

## Step 3: Data Splitting

The next step is to split the data into training and testing sets. We will use 80% of the data for training and 20% for testing. We use the `train_test_split` function from the `sklearn` library to do this.

## Step 4: Data Vectorization

We now need to convert the text data into numerical data that the machine learning model can understand. This is done using the TF-IDF vectorizer.

### TF-IDF

TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.

<details>
<summary>Calculations details</summary>
Term Frequency of a word in a document = (Number of times the `word` appears in the document) / (Total number of words in the document)

Inverse Document Frequency of a word = log((Total number of documents) / (Number of documents containing the `word`))

TF-IDF of a word in a document = (Term Frequency of the word in the document) \* (Inverse Document Frequency of the `word`)

</details>

We use the `TfidfVectorizer` class from the `sklearn` library to convert the text data into TF-IDF vectors.
This class has a `transform` and a `fit_transform` methods that can be used to convert the text data into numerical matrices.
We first apply the `fit_transform` method on the training data so the vectorizer learns the vocabulary and the IDF from the training data `x_train`. It then transformes this data into a numerical matrix representation.
We then apply the same transformation learned from the training data on the testing data `x_test` using the `transform` method. This ensures that the testing data is transformed in the same way as the training data using the same vocabulary and IDF values.

## Step 5: Model Training

We will use multiple models to train on the data:

- Logistic Regression
- Random Forest
- Naive Bayes

We will use the `fit` method to train the model on the training data. This method takes the training data `x_train` and the training labels `y_train` as input. The model will learn the patterns in the training data and use them to make predictions on new data.
The trained models and the vectorizer are saved using the `joblib` library so they can be used later for making predictions.

## Step 6: Model Evaluation

We will evaluate the models using the testing data. We will use the `accuracy_score` function from the `sklearn` library to calculate the accuracy of the model on the testing data. The accuracy is the percentage of correct predictions made by the model. We will also use the `classification_report` function to get a detailed report of the model's performance. This report includes precision, recall, f1-score, and support for each class.

## Step 7: Model Comparison

We have added functionality to compare the performance of different models graphically. This includes plotting accuracy, precision, recall, and F1-score for each model.
The functions for comparing the models are located in a separate file, `comparison_functions.py`.

## Step 8: Making Predictions

We will use the trained models to make predictions on new data. We will use the `predict` method of the model to make predictions on the new data. The `predict` method takes the new data as input and returns the predicted labels. We will also use the `predict_proba` method to get the probabilities of each class for each prediction.
