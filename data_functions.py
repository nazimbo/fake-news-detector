import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re


def prepare_data(df_fake, df_true):

    # Adding a label column
    df_fake["label"] = 1
    df_true["label"] = 0

    # Removing the useless columns
    df_fake = df_fake.drop(["title", "subject", "date"], axis=1)
    df_true = df_true.drop(["title", "subject", "date"], axis=1)

    # Merging the two datasets
    df = pd.concat([df_fake, df_true])

    # Checking for missing values
    print(f'''Missing values:
    {df.isnull().sum()}
        ''')

    print(f"Fake news: {df['label'].value_counts()[1]}")
    print(f"True news: {df['label'].value_counts()[0]}")

    # Shuffling the dataset
    df = df.sample(frac=1).reset_index(drop=True)

    return df


def clean_text(text):
    text = text.lower()
