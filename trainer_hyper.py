from joblib import dump
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the cleaned dataset
dataset = pd.read_csv("dataset/cleaned_dataset.csv")

# Split the dataset into features and labels
x, y = dataset["text"], dataset["label"]

# Split the dataset into training and testing sets (80% training, 20% testing)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the training data
x_train_vectorized = vectorizer.fit_transform(x_train)
x_test_vectorized = vectorizer.transform(x_test)

# Define models with their respective hyperparameter grids
models = {
    "Logistic Regression": (LogisticRegression(random_state=42),
                            {'C': [0.1, 1.0, 10.0], 'max_iter': [100, 500, 1000], 'solver': ['liblinear', 'lbfgs']}),

    "Naive Bayes": (MultinomialNB(),
                    {'alpha': [0.1, 0.5, 1.0]}),

    "Random Forest": (RandomForestClassifier(random_state=42),
                      {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10]})
}

# Save the vectorizer
dump(vectorizer, 'models_hyperparams/vectorizer.joblib')

# Train, tune hyperparameters, and save each model
for model_name, (model, param_grid) in models.items():
    print(f"Training {model_name}...")
    grid_search = GridSearchCV(
        model, param_grid, cv=5, scoring='accuracy', verbose=1, n_jobs=-1)
    grid_search.fit(x_train_vectorized, y_train)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Predictions
    y_pred = best_model.predict(x_test_vectorized)

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model_name} Accuracy: {accuracy}")
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # Save the best model
    dump(best_model,
         f'models_hyperparams/best_model_{model_name.replace(" ", "_").lower()}.joblib')
