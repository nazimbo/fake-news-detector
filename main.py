from data_functions import prepare_data
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

fake_news = pd.read_csv("dataset/fake.csv")
true_news = pd.read_csv("dataset/true.csv")

df = prepare_data(fake_news, true_news)
print(df.head(20))
