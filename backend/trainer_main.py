from joblib import dump
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os
from comparison_functions import (
    plot_roc_curve,
    plot_confusion_matrix,
    plot_classification_report,
)

# PART 2 - MODEL TRAINING
# Load the cleaned dataset
dataset = pd.read_csv("dataset/cleaned_dataset.csv")

# Split the dataset into features and labels
x, y = dataset["text"], dataset["label"]

# Split the dataset into training and testing sets (80% training, 20% (0.2) testing)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the training data
x_train_vectorized = vectorizer.fit_transform(x_train)
x_test_vectorized = vectorizer.transform(x_test)

# Define models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Naive Bayes": MultinomialNB(),
    "Random Forest": RandomForestClassifier(random_state=42),
}

# Save the vectorizer
os.makedirs("models", exist_ok=True)
dump(vectorizer, "models/vectorizer.joblib")

# Train and save each model
for model_name, model in models.items():
    model.fit(x_train_vectorized, y_train)
    y_pred = model.predict(x_test_vectorized)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model_name} Accuracy: {accuracy}")
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # Save the model
    dump(model, f'models/model_{model_name.replace(" ", "_").lower()}.joblib')

# Create directory for graphics
os.makedirs("graphics", exist_ok=True)

# Generate comparison graphics
plot_roc_curve(models, x_test_vectorized, y_test, "graphics/roc_curve.png")
plot_confusion_matrix(
    models, x_test_vectorized, y_test, "graphics/confusion_matrix.png"
)
plot_classification_report(
    models, x_test_vectorized, y_test, "graphics/classification_report.png"
)
