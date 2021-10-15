from keras.preprocessing.image import ImageDataGenerator
import keras
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from keras.regularizers import l2


train_datagen = ImageDataGenerator(

      rescale=1./255,

      rotation_range=40,

      width_shift_range=0.2,

      height_shift_range=0.2,

      shear_range=0.2,

      zoom_range=0.2,

      horizontal_flip=True,

      fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)


class MyModel(tf.keras.Model):

  def __init__(self):
    super(MyModel, self).__init__()

    self.cnn1 = tf.keras.layers.Conv2D(96, (11, 11), activation='relu', input_shape=(155,220,1))
    self.batch1 =tf.keras.layers.BatchNormalization(epsilon=1e-08, axis=1, momentum=0.9)
    self.max1 =tf.keras.layers.MaxPooling2D(pool_size=(3,3), strides=(2, 2))
    self.zero1 =tf.keras.layers.ZeroPadding2D(padding=(2,2), data_format=None)

    self.cnn2 = tf.keras.layers.Conv2D(128, (5, 5), activation='relu')
    self.batch2 =tf.keras.layers.BatchNormalization(epsilon=1e-06, axis=1, momentum=0.9)
    self.max2 =tf.keras.layers.MaxPooling2D(pool_size=(3,3), strides=(2, 2))
    self.drop1=tf.keras.layers.Dropout(0.3)
    self.zero2 =tf.keras.layers.ZeroPadding2D(padding=(2,2), data_format=None)

    self.cnn3 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu')
    self.zero3 =tf.keras.layers.ZeroPadding2D(padding=(3,3), data_format=None)


    self.cnn4 =tf.keras.layers.Conv2D(128, (3, 3), activation='relu')
    self.max3 =tf.keras.layers.MaxPooling2D(pool_size=(3,3), strides=(2, 2))
    self.drop2=tf.keras.layers.Dropout(0.3)
    self.flatten = tf.keras.layers.Flatten()
    self.dense1 = tf.keras.layers.Dense(512, bias_regularizer=l2(0.0005), activation='relu')
    self.drop3=tf.keras.layers.Dropout(0.5)
    self.dense2 = tf.keras.layers.Dense(1, activation='sigmoid')
  def call(self, inputs):
    
    x = self.cnn1(inputs)
    x = self.batch1(x)
    x = self.max1(x)
    x = self.zero1(x)
    x = self.cnn2(x)
    x = self.batch2(x)
    x = self.max2(x)
    x = self.drop1(x)
    x = self.zero2(x)
    x = self.cnn3(x)
    x = self.zero3(x)
    x = self.cnn4(x)
    x = self.max3(x)
    x = self.drop2(x)
    x = self.flatten(x)
    x = self.dense1(x)
    x = self.drop3(x)
    x = self.dense2(x)
    return x

model = MyModel()

input_shape = (None, 155, 220, 1)
model.build(input_shape)

rms=tf.keras.optimizers.RMSprop(learning_rate=1e-4, rho=0.9, epsilon=1e-08)
adam= tf.keras.optimizers.Adam(learning_rate=1e-4,
    beta_1=0.9,
    beta_2=0.999,
    amsgrad=False)
model.compile(
    loss="binary_crossentropy",

    optimizer=rms,
   

    metrics=["acc"])

import dill as pickle

with open('name_model.pkl', 'rb') as file:
    B = pickle.load(file)


test_dir2 = os.path.join("Test/") 

test_generator2 = test_datagen.flow_from_directory(

        test_dir2,

        target_size=(155, 220),

        batch_size=1,
        color_mode="grayscale",

        class_mode='binary')

test_input = test_generator2[0][0][0] 
test_input = np.expand_dims(test_input,axis=0)
pred2=B.predict(model ,test_input, batch_size=None, verbose=0, steps=None, callbacks=None, max_queue_size=10, workers=1, use_multiprocessing=False)
if(pred2<0.4956):
  print('signature authentique')
else:
  print('signature imitée')