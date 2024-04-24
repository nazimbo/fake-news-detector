from sklearn.model_selection import train_test_split
from data_functions import *
import pandas as pd


# fake_news = pd.read_csv("dataset/fake.csv")
# true_news = pd.read_csv("dataset/true.csv")

# dataset = prepare_data(fake_news, true_news)

# # Apply the clean_text function to each element in the text column
# dataset["text"] = dataset["text"].apply(lambda x: clean_text(x))

# print(dataset.head(20))

# # Save the cleaned dataset
# dataset.to_csv("dataset/cleaned_dataset.csv", index=False)


# Load the cleaned dataset
dataset = pd.read_csv("dataset/cleaned_dataset.csv")
print(dataset.head(20))

# Split the dataset into features and labels
x, y = dataset["text"], dataset["label"]

# Split the dataset into training and testing sets (80% training, 20% (0.2) testing)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2)

print(f"Training set: {x_train.shape[0]} samples")
print(f"Testing set: {x_test.shape[0]} samples")
print(f"Training labels: {y_train.shape[0]} samples")
print(f"Testing labels: {y_test.shape[0]} samples")
