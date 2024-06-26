import os
import json
from joblib import load
from data_functions import clean_text
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from colorama import init, Fore, Style
from termcolor import colored

# Initialize colorama
init()

# Define the directory containing the models
model_directory = 'models/'

# Load the vectorizer
vectorizer = load(f'{model_directory}/vectorizer.joblib')

# Load the test articles from the JSON file
with open('test_articles.json', 'r') as file:
    data = json.load(file)

# Extract texts and true labels
texts = [article["text"] for article in data["articles"]]
true_labels = [1 if article["label"] ==
               "fake" else 0 for article in data["articles"]]

# Clean the texts
cleaned_texts = [clean_text(text) for text in texts]

# Transform the texts using the vectorizer
vectorized_texts = vectorizer.transform(cleaned_texts)

# List all model files in the model directory
model_filenames = [f for f in os.listdir(
    model_directory) if f.endswith('.joblib') and f != 'vectorizer.joblib']

# Evaluate each model
for model_filename in model_filenames:
    # Load the model
    model_path = os.path.join(model_directory, model_filename)
    model = load(model_path)

    # Predict using the model
    predicted_labels = model.predict(vectorized_texts)

    # Convert predicted labels from numeric to string for display
    predicted_labels_str = ['fake' if label ==
                            1 else 'true' for label in predicted_labels]
    true_labels_str = ['fake' if label ==
                       1 else 'true' for label in true_labels]

    # Evaluate the predictions
    accuracy = accuracy_score(true_labels, predicted_labels)
    model_name = model_filename.replace('model_', '').replace(
        '.joblib', '').replace('_', ' ').title()
    print(colored(f"{model_name} Accuracy: {accuracy}",
          'green' if accuracy > 0.7 else 'red'))
    print(Fore.YELLOW + classification_report(true_labels,
          predicted_labels) + Style.RESET_ALL)
    print(Fore.CYAN + str(confusion_matrix(true_labels,
          predicted_labels)) + Style.RESET_ALL)

    # Print the predictions alongside the true labels and texts
    for text, true_label, predicted_label in zip(texts, true_labels_str, predicted_labels_str):
        print(Fore.MAGENTA + f"Text: {text}" + Style.RESET_ALL)
        true_label_color = 'green' if true_label == predicted_label else 'red'
        predicted_label_color = 'green' if true_label == predicted_label else 'red'
        print(f"True Label: {colored(true_label, true_label_color)}, Predicted Label: {colored(predicted_label, predicted_label_color)}\n")
