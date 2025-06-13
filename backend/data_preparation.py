import pandas as pd
from data_functions import *

# PART 1 - DATA PREPARATION
# Load datasets
fake_news = pd.read_csv("dataset/fake.csv")
true_news = pd.read_csv("dataset/true.csv")

# Prepare the dataset
dataset = prepare_data(fake_news, true_news)

# Apply the clean_text function to each element in the text column
dataset["text"] = dataset["text"].apply(lambda x: clean_text(x))

# Print the first 20 rows for inspection
print(dataset.head(20))

# Remove the rows with empty text
dataset = dataset[dataset["text"] != ""]

# Save the cleaned dataset
dataset.to_csv("dataset/cleaned_dataset.csv", index=False)
