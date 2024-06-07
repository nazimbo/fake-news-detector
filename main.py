from sklearn.naive_bayes import MultinomialNB
from joblib import dump
from data_functions import *
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# PART 2 - MODEL TRAINING
# Load the cleaned dataset
dataset = pd.read_csv("dataset/cleaned_dataset.csv")

# Split the dataset into features and labels
x, y = dataset["text"], dataset["label"]

# Split the dataset into training and testing sets (80% training, 20% (0.2) testing)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the training data
x_train_vectorized = vectorizer.fit_transform(x_train)
x_test_vectorized = vectorizer.transform(x_test)

# Initialize the Logistic Regression model (UNCOMMENT TO USE)
model = LogisticRegression(max_iter=1000, random_state=42)

# Train the model
model.fit(x_train_vectorized, y_train)

# Test the model
y_pred = model.predict(x_test_vectorized)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Display the classification report
print(classification_report(y_test, y_pred))

# Display the confusion matrix
print(confusion_matrix(y_test, y_pred))


# Save the model
dump(model, 'model_logistic.joblib')

# Save the vectorizer
dump(vectorizer, 'vectorizer.joblib')
