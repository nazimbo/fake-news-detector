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

    # Checking the number of fake and true news
    print(f"Fake news: {df['label'].value_counts()[1]}")
    print(f"True news: {df['label'].value_counts()[0]}")

    # Shuffling the dataset
    df = df.sample(frac=1).reset_index(drop=True)

    return df


def clean_text(text):
    # Converting the text to lowercase
    text = text.lower()

    # Removing URLs
    text = re.sub(r'http\S+', '', text)

    # Removing non-alphabetic characters
    text = re.sub(r'[^a-zA-Z]', ' ', text)

    # Tokenization (splitting the text into words)
    text = text.split()

    # Removing stopwords (common words that do not carry much information, such as 'the', 'a', 'is')
    stop_words = set(stopwords.words("english"))
    text = [word for word in text if word not in stop_words]

    # Lemmatization (converting words to their base form, such as 'running' to 'run')
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text]

    cleaned_text = " ".join(text)

    return cleaned_text
