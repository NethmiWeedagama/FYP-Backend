# from string import punctuation
import string
import zipfile

from flask import jsonify

string.punctuation
import re
from nltk.stem.porter import PorterStemmer

# defining the object for stemming
porter_stemmer = PorterStemmer()
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# defining the object for Lemmatization
wordnet_lemmatizer = WordNetLemmatizer()
from keras.models import load_model



import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import os

from keras.models import Sequential

from tensorflow.keras.layers import Dense,Dropout,Flatten, BatchNormalization
from keras.regularizers import l2
from keras import optimizers
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import f1_score
from sklearn import metrics
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
def preprocess_text(text):
    """ Apply preprocessing methods"""
    punctuationfree = "".join([i for i in text if i not in string.punctuation])
    #     text = punctuationfree.lower()
    #     translator = str.maketrans('', '', string.punctuation)
    text = punctuationfree.lower()

    result = re.sub(r'\d+', '', text)

    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    removed_url = url_pattern.sub(r'', result)
    html_pattern = re.compile('<.*?>')
    removed_tag = html_pattern.sub(r'', removed_url)

    #     removed_special_char
    tokens = re.split('W+', str(removed_tag))
    stemmer = PorterStemmer()
    stem_text = " ".join([stemmer.stem(word) for word in tokens])
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
    return lemm_text

def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict

# def loadmodel():
#     # try:
#     #     zip_file_path = "D://University/IIT/level 6/FYP IMPLEMENTATION/FYP-BACKEND/model/priority model.zip"
#     #     model_file_name = 'priority model.h5'
#     #
#     #     # Extract the model file from the zip file
#     #     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     #         zip_ref.extract(model_file_name)
#
#         loaded_model = load_model("D://University/IIT/level 6/FYP/BackendFyp/model/priority model.h5")
#         # loaded_model = load_model(model_file_name)
#         return loaded_model
#     # except Exception as e:
#     #     # Return error message with status code 500
#     #     return jsonify({'message': 'Error .Please try again'}),
#
# def loadmodelSeverity():
#
#     # zip_file_path = "D://University/IIT/level 6/FYP IMPLEMENTATION/FYP-BACKEND/model/modelSeverity3SmotENN.zip"
#     # model_file_name = 'modelSeverity3SmotENN.h5'
#     #
#     # # Extract the model file from the zip file
#     # with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     #     zip_ref.extract(model_file_name)
#     #
#     # # loaded_model = load_model("D://University/IIT/level 6/FYP/BackendFyp/model/priority model.h5")
#     # loaded_modelSeverity = load_model(model_file_name)
#     loaded_modelSeverity = load_model("D://University/IIT/level 6/FYP/BackendFyp/model/modelSeverity3SmotENN.h5")
#     return loaded_modelSeverity