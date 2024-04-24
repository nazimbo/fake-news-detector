# Fake News Detector

This project is a fake news detector that uses a machine learning model to classify news articles as fake or real. The model is trained on a dataset of news articles that are labeled as fake or real.

## Dataset

The dataset used to train the model is from Kaggle (https://www.kaggle.com/code/therealsampat/fake-news-detection/input). The dataset contains two CSV files, one with fake news articles and one with real news articles.

## Step 1: Data Preparing

The first step is to prepare the data for training the model. This involves loading the data, removing useless columns, adding a label to each article (fake or real), and combining the two datasets into one shuffled dataset. The function `prepare_data` in `data_functions.py` does this.

## Step 2: Data Cleaning

The next step is to clean the data. This involves lowercasing the text, replacing all non alphabetical characters with spaces, removing stopwords, and lemmatizing the text. The function `clean_data` in `data_functions.py` does this.

## Step 3: Feature Extraction

We now need to convert the text data into numerical data that the machine learning model can understand. This is done using the TF-IDF vectorizer.
TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.

Term Frequency of a word in a document = (Number of times the `word` appears in the document) / (Total number of words in the document)

Inverse Document Frequency of a word = log((Total number of documents) / (Number of documents containing the `word`))

TF-IDF of a word in a document = (Term Frequency of the word in the document) \* (Inverse Document Frequency of the `word`)
