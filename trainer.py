from joblib import dump
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

# Split the dataset into training and testing sets (80% training, 20% testing)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.95)

# Fit and transform the training data
x_train_vectorized = vectorizer.fit_transform(x_train)
x_test_vectorized = vectorizer.transform(x_test)

# Initialize the Logistic Regression model
model = LogisticRegression(max_iter=1000, random_state=42)

# Hyperparameter tuning with GridSearchCV
param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],
    'penalty': ['l2'],
    'solver': ['lbfgs', 'liblinear']
}
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(x_train_vectorized, y_train)

# Get the best model from grid search
model = grid_search.best_estimator_

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
