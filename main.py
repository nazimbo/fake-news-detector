from data_functions import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


# fake_news = pd.read_csv("dataset/fake.csv")
# true_news = pd.read_csv("dataset/true.csv")

# dataset = prepare_data(fake_news, true_news)

# # Apply the clean_text function to each element in the text column
# dataset["text"] = dataset["text"].apply(lambda x: clean_text(x))

# print(dataset.head(20))

# # remove the rows with empty text
# dataset = dataset[dataset["text"] != ""]

# # Save the cleaned dataset
# dataset.to_csv("dataset/cleaned_dataset.csv", index=False)


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
