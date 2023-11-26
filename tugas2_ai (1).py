# -*- coding: utf-8 -*-
"""Tugas2_AI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yp8wgFNo0fdQG1WAuaLJUNnTDpHl7iNC
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer
import tensorflow.keras as k
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import TensorBoard

data = pd.read_csv('/content/data.csv')

data.head()

data.isnull().sum()

data,test = train_test_split(data,test_size = 0.2)

data,validation = train_test_split(data,test_size = 0.2)

data.shape

test.shape

data = data.drop(columns = ['id'])

data['diagnosis'].unique()

labels = data['diagnosis']

data.drop(columns = ['diagnosis'],inplace = True)

data = data.iloc[:,0:29]

data.head()

daig = validation['diagnosis']
validation.drop(columns = ['id','diagnosis'],inplace=True)
validation.iloc[:,0:29]

validation = validation.iloc[:,0:29]

"""Data Preparation for model training"""

n = Normalizer()

data_x = data

data_x.shape

data_x = n.fit_transform(data_x)

map = {'M':1,'B':0}

labels.value_counts()

labels = labels.map(map)

labels

validation = n.transform(validation)

daig = daig.map(map)

test.head()

test_y = test['diagnosis']

test = test.drop(columns = ['id','diagnosis'])

test= test.iloc[:,0:29]

test.head()

test = n.transform(test)

test_y = test_y.map(map)

test_y.head()

# Setting up TensorBoard
log_dir = '/tmp/tensorboard_logs'
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

"""**Building and Training a Neural Network**"""

import keras as k

# Define the number of epochs
epoch = 120

# Create a sequential model
model = k.models.Sequential([
    k.layers.Dense(12, input_dim=29, activation='relu'),
    k.layers.Dropout(0.5),
    k.layers.Dense(5, activation='relu'),
    k.layers.Dropout(0.5),
    k.layers.Dense(1, activation='sigmoid')
])

# Define a model checkpoint callback
model_check = k.callbacks.ModelCheckpoint('model_check.h5', save_best_only=True)

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model to the data (with verbose=1 to print epochs)
history = model.fit(data_x, labels, epochs=epoch, verbose=1, validation_data=(validation, daig), callbacks=[model_check, tensorboard_callback])

model = k.models.load_model('model_check.h5')

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(1,epoch+1)

plt.figure(figsize = (30,30))
plt.subplot(2,1,1)
plt.plot(epochs_range,acc,label = 'training_acc')
plt.plot(epochs_range,val_acc,label = 'val_acc')
plt.legend(loc = 'lower right',fontsize = 30)
plt.title('Training and Validation Accuracy',fontsize = 30)
plt.subplot(2,1,2)
plt.plot(epochs_range,loss,label = 'training_loss')
plt.plot(epochs_range,val_loss,label = 'val_loss')
plt.legend(loc = 'lower right',fontsize = 30)
plt.title('Training and Validation Loss',fontsize = 30)

predictions = model.predict(test)

pred = []
for i in range(0,len(predictions)):
  if predictions[i][0]>=0.5:
    pred.append(1)
  else:
    pred.append(0)

from sklearn.metrics import accuracy_score
accuracy_score(test_y,pred)

predictions_train = model.predict(data_x)

pred_train = []
for i in range(0,len(predictions_train)):
  if predictions_train[i][0]>=0.5:
    pred_train.append(1)
  else:
    pred_train.append(0)

accuracy_score(labels,pred_train)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir /tmp/tensorboard_logs

