# Fake News Detector

This project is a fake news detector that uses a machine learning model to classify news articles as fake or real. The model is trained on a dataset of news articles that are labeled as fake or real.

## Dataset

The dataset used to train the model is from Kaggle (https://www.kaggle.com/code/therealsampat/fake-news-detection/input). The dataset contains two CSV files, one with fake news articles and one with real news articles.

## Step 1: Data Preparing

The first step is to prepare the data for training the model. This involves loading the data, removing useless columns, adding a label to each article (fake or real), and combining the two datasets into one shuffled dataset. The function `prepare_data` in `data_functions.py` does this.

## Step 2: Data Cleaning

The next step is to clean the data. This involves lowercasing the text, replacing all non alphabetical characters with spaces, removing stopwords, and lemmatizing the text. The function `clean_data` in `data_functions.py` does this.

## Step 3: Data Splitting

The next step is to split the data into training and testing sets. We will use 80% of the data for training and 20% for testing. We use the `train_test_split` function from the `sklearn` library to do this.

## Step 4: Data Vectorization

We now need to convert the text data into numerical data that the machine learning model can understand. This is done using the TF-IDF vectorizer.

### TF-IDF

TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.

<details>
<summary>Calculations details</summary>
Term Frequency of a word in a document = (Number of times the `word` appears in the document) / (Total number of words in the document)

Inverse Document Frequency of a word = log((Total number of documents) / (Number of documents containing the `word`))

TF-IDF of a word in a document = (Term Frequency of the word in the document) \* (Inverse Document Frequency of the `word`)

</details>

We use the `TfidfVectorizer` class from the `sklearn` library to convert the text data into TF-IDF vectors.
This class has a `transform` and a `fit_transform` methods that can be used to convert the text data into numerical matrices.
We first apply the `fit_transform` method on the training data so the vectorizer learns the vocabulary and the IDF from the training data `x_train`. It then transformes this data into a numerical matrix representation.
We then apply the same transformation learned from the training data on the testing data `x_test` using the `transform` method. This ensures that the testing data is transformed in the same way as the training data using the same vocabulary and IDF values.

## Step 5: Model Training

We will use the `LogisticRegression` class from the `sklearn` library to train the model. We first create an instance of the `LogisticRegression` class and then call the `fit` method on the training data to train the model.
