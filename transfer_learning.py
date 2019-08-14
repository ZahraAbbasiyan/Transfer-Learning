# -*- coding: utf-8 -*-
"""Transfer_learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XLTSLwI2AFUkuEPraW6PZQb8ZXBzH9fs
"""

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import tensorflow.keras as keras
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
import tensorflow as tf
from keras.utils import np_utils
from keras.models import load_model
from keras.datasets import cifar10
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

resnet_net = ResNet50(weights='imagenet', include_top=False, input_shape=(200, 200, 3))

print(resnet_net.summary())

resnet_net.trainable = True

print("Number of layers in the resnet model: ", len(resnet_net.layers))


freeze_layers = 100

for layer in resnet_net.layers[:freeze_layers]:
  layer.trainable =  False

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

x_train = -1*(x_train / 255.0)
x_test = -1*(x_test / 255.0)

x_train = x_train[0:500]
x_test = x_test[0:100]


y_train = np_utils.to_categorical(y_train, 10)
y_test = np_utils.to_categorical(y_test, 10)

y_train = y_train[0:500]
y_test = y_test[0:100]

print(x_train.shape)
print(x_test.shape)

import numpy as np
from matplotlib import pyplot as plt
from IPython.display import clear_output

class PlotLosses(keras.callbacks.Callback):
  
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        
        self.fig = plt.figure()
        
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1
        
        clear_output(wait=True)
        plt.plot(self.x, self.losses, label="loss")
        plt.plot(self.x, self.val_losses, label="val_loss")
        plt.legend()
        plt.show();
        
plot_losses = PlotLosses()

model = models.Sequential()

model.add(layers.UpSampling2D((2,2)))
model.add(layers.UpSampling2D((2,2)))
model.add(layers.UpSampling2D((2,2)))

model.add(resnet_net)
model.add(layers.Flatten())
model.add(layers.BatchNormalization())


model.add(layers.Dense(10, activation='softmax'))

# filepath="model/resnet.model"

# checkpoint = keras.callbacks.ModelCheckpoint(
#     filepath, verbose=1, monitor='val_loss', save_best_only=True, mode='auto')  



model.compile(optimizer=keras.optimizers.Adam(lr=0.2), loss='binary_crossentropy', metrics=['acc'])


history = model.fit(x_train, y_train, epochs=10, batch_size=50,
                    callbacks=[plot_losses],
                    validation_data=(x_test, y_test))

model.save('my_model.h5')

model.evaluate(x_test, y_test)

history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']

epochs = range(1, len(loss_values) + 1)

plt.plot(epochs, loss_values,  label='train')
plt.plot(epochs, val_loss_values,  label='validation Loss')
plt.title('train and validation loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()

acc = history_dict['acc']
val_acc = history_dict['val_acc']

epochs = range(1, len(loss_values) + 1)

plt.show()

plt.plot(epochs, acc, label='train accuracy')
plt.plot(epochs, val_acc,  label='validation accuracy')
plt.title('train and validation accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()

history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']

epochs = range(1, len(loss_values) + 1)

plt.plot(epochs, loss_values,  label='train')
plt.plot(epochs, val_loss_values,  label='validation Loss')
plt.title('train and validation loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()

acc = history_dict['acc']
val_acc = history_dict['val_acc']

epochs = range(1, len(loss_values) + 1)


plt.plot(epochs, acc, label='train accuracy')
plt.plot(epochs, val_acc,  label='validation accuracy')
plt.title('train and validation accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()

model.evaluate(x_train, y_train)