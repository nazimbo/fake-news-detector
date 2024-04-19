from data_functions import *
import pandas as pd


fake_news = pd.read_csv("dataset/fake.csv")
true_news = pd.read_csv("dataset/true.csv")

df = prepare_data(fake_news, true_news)
print(df.head(20))
