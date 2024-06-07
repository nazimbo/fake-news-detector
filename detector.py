import json
from joblib import load
from data_functions import clean_text
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from colorama import init, Fore, Style
from termcolor import colored

# Initialize colorama
init()

# Load the model and vectorizer
model = load('model_logistic.joblib')
vectorizer = load('vectorizer.joblib')

# Load the test articles from the JSON file
with open('test_articles.json', 'r') as file:
    data = json.load(file)

# Extract texts and true labels
texts = [article["text"] for article in data["articles"]]
# Converting labels to numeric format for evaluation
true_labels = [1 if article["label"] ==
               "fake" else 0 for article in data["articles"]]

# Clean the texts
cleaned_texts = [clean_text(text) for text in texts]

# Transform the texts using the vectorizer
vectorized_texts = vectorizer.transform(cleaned_texts)

# Predict using the model
predicted_labels = model.predict(vectorized_texts)

# Convert predicted labels from numeric to string for display
predicted_labels_str = ['fake' if label ==
                        1 else 'true' for label in predicted_labels]
true_labels_str = ['fake' if label == 1 else 'true' for label in true_labels]

# Evaluate the predictions
accuracy = accuracy_score(true_labels, predicted_labels)
print(colored(f"Accuracy: {accuracy}", 'green' if accuracy > 0.7 else 'red'))
print(Fore.YELLOW + classification_report(true_labels,
      predicted_labels) + Style.RESET_ALL)
print(Fore.CYAN + str(confusion_matrix(true_labels, predicted_labels)) + Style.RESET_ALL)

# Print the predictions alongside the true labels and texts
for text, true_label, predicted_label in zip(texts, true_labels_str, predicted_labels_str):
    print(Fore.MAGENTA + f"Text: {text}" + Style.RESET_ALL)
    true_label_color = 'green' if true_label == predicted_label else 'red'
    predicted_label_color = 'green' if true_label == predicted_label else 'red'
    print(f"True Label: {colored(true_label, true_label_color)}, Predicted Label: {
          colored(predicted_label, predicted_label_color)}\n")
