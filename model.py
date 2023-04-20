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

def model():
    model = tf.keras.Sequential()

    # model.add(tf.keras.layers.Dense(units=300, activation='relu', input_shape=[3,]))
    model.add(tf.keras.layers.Dense(2000, input_dim=3, activation='relu'))
    model.add(tf.keras.layers.Dense(units=3000, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(tf.keras.layers.Dense(units=4000, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(tf.keras.layers.Dense(units=5000, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(tf.keras.layers.Dense(units=3000, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(tf.keras.layers.Dense(units=3, activation='softmax'))

    model.compile(Adam(learning_rate=0.0001), "sparse_categorical_crossentropy",
                  metrics=["sparse_categorical_accuracy"])
    model.summary()
    # from keras.wrappers.scikit_learn import KerasClassifier
    # from sklearn.model_selection import cross_val_score
    # from sklearn.model_selection import KFold
    hist = model.fit(X_train, Y_train, batch_size=64, verbose=2, epochs=1000)