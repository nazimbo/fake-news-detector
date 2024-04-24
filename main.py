from data_functions import *
import pandas as pd


fake_news = pd.read_csv("dataset/fake.csv")
true_news = pd.read_csv("dataset/true.csv")

dataset = prepare_data(fake_news, true_news)
print(dataset.head(20))

# Apply the clean_text function to each element in the text column
dataset["text"] = dataset["text"].apply(lambda x: clean_text(x))
print(dataset.head(20))
